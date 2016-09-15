#!/usr/bin/env python

import numpy as np
import os
import pandas as pd
import sys


def abide_motion_wrapper(motion_thresh, age_l, age_u, n, n_perms=1000, overwrite=True):
    behav_data_f = '../../Phenotypic_V1_0b_preprocessed1.csv'
       
    f_name = 'RESULTS/rsq_{:03.0f}pct_{:03.0f}subs_{:02.0f}to{:02.0f}.csv'.format(motion_thresh, n, age_l, age_u)
    
    # By default this code will recreate files even if they already exist
    # (overwrite=True)
    # If you don't want to do this though, set overwrite to False and 
    # this step will skip over the analysis if the file already exists
    if not overwrite:
        # If the file exists then skip this loop
        if os.path.isfile(f_name):
            return
    
    df = read_in_data(behav_data_f)

    rsq_list = split_half_outcome(df, motion_thresh, age_l, age_u, n, n_perms=n_perms)

    med_rsq = np.median(rsq_list)
    rsq_CI = np.percentile(rsq_list, 97.5) - np.percentile(rsq_list, 2.5)

    columns = [ 'motion_thresh', 'age_l', 'age_u', 'n', 'med_rsq', 'CI_95' ]
    results_df = pd.DataFrame(np.array([[motion_thresh, age_l, age_u, n, med_rsq, rsq_CI]]), 
                                  columns=columns)


    results_df.to_csv(f_name)

    
def read_in_data(behav_data_f):
    """
    Read in the data
    """
    df = pd.read_csv(behav_data_f)
    df = df.loc[df['func_perc_fd'].notnull(), :]
    df = df.loc[df['FILE_ID']!='no_filename', :]
    df['AGE_YRS'] = np.floor(df['AGE_AT_SCAN'])

    return df


def split_half_outcome(df, motion_thresh, age_l, age_u, n, n_perms=100):
    
    """
    This function returns the R squared of how each parameter affects split-half reliability!
    It takes in a dataframe, motion threshold, an age upper limit(age_u) an age lower limit (age_l), sample size (n),
    and number of permutations (n_perms, currently hard coded at 100). This function essentially splits a data frame 
    into two matched samples (split_two_matched_samples.py), then creates mean roi-roi correlation matrices per sample 
    (make_group_corr_mat.py) and then calculates the R squared (calc_rsq.py) between the two samples'
    correlation matrices and returns all the permuation coefficients of determinations in a dataframe.
    """
    
    #set up data frame of average R squared to fill up later
    Rsq_list = []
    
    #Do this in each permutation
    for i in range(n_perms):
        #create two matched samples split on motion_thresh, age upper, age lower, and n
        df_A, df_B = split_two_matched_samples(df, motion_thresh, age_l, age_u, n)
        #make the matrix of all subjects roi-roi correlations, make the mean corr mat, and make covariance cor mat
        #do this for A and then B
        all_corr_mat_A, av_corr_mat_A, var_corr_mat_A = make_group_corr_mat(df_A)
        all_corr_mat_B, av_corr_mat_B, var_corr_mat_B = make_group_corr_mat(df_B)
        
        #calculate the R squared between the two matrices
        Rsq = calc_rsq(av_corr_mat_A, av_corr_mat_B)

        #build up R squared output
        Rsq_list += [Rsq]
    
    return np.array(Rsq_list)


def calc_rsq(av_corr_mat_A, av_corr_mat_B):
    """
    From wikipedia: https://en.wikipedia.org/wiki/Coefficient_of_determination
    
    Rsq = 1 - (SSres / SStot)
    
    SSres is calculated as the sum of square errors (where the error
    is the difference between x and y).
    
    SStot is calculated as the total sum of squares in y.
    """
    # Get the data we need
    inds = np.triu_indices_from(av_corr_mat_B, k=1)
    x = av_corr_mat_A[inds]
    y = av_corr_mat_B[inds]
    
    # Calculate the error/residuals
    res = y - x

    SSres = np.sum(res**2)
    
    # Sum up the total error in y
    y_var = y - np.mean(y)
    
    SStot = np.sum(y_var**2)
    
    # R squared
    Rsq = 1 - (SSres/SStot)
    
    return Rsq

def exclude_nan(x,y):
    """
    Exclude NaN values if either entry in a pair of vectors has NaN
    """
    idx = np.logical_not(np.logical_or(np.isnan(x), np.isnan(y)))
    x = x[idx]
    y = y[idx]
    n = len(x)
    return [x, y, n]

def compute_icc(av_corr_mat_A, av_corr_mat_B):
    """
    This function computes the inter-class correlation (ICC) of the
    two classes represented by the x and y numpy vectors.
    """

    inds = np.triu_indices_from(av_corr_mat_B, k=1)
    x = av_corr_mat_A[inds]
    y = av_corr_mat_B[inds]
    
    if all(x == y):
        return 1

    [x, y, n] = exclude_nan(x,y)

    ## Need at least 3 data points to compute this
    if n < 3:
        return np.nan

    Sx = sum(x); Sy = sum(y);
    Sxx = sum(x*x); Sxy = sum( (x+y)**2 )/2; Syy = sum(y*y)

    fact = ((Sx + Sy)**2)/(n*2)
    SS_tot = Sxx + Syy - fact
    SS_among = Sxy - fact
    SS_error = SS_tot - SS_among

    MS_error = SS_error/n
    MS_among = SS_among/(n-1)
    ICC = (MS_among - MS_error) / (MS_among + MS_error)

    return ICC

def make_group_corr_mat(df):
    """
    This function reads in each subject's aal roi time series files and creates roi-roi correlation matrices
    for each subject and then sums them all together. The final output is a 3d matrix of all subjects 
    roi-roi correlations, a mean roi-roi correlation matrix and a roi-roi covariance matrix. 
    **NOTE WELL** This returns correlations transformed by the Fisher z, aka arctanh, function.    
    """

    # for each subject do the following
    
    for i, (sub, f_id) in enumerate(df[['SUB_ID', 'FILE_ID']].values):
        
        #read each subjects aal roi time series files
        ts_df = pd.read_table('DATA/{}_rois_aal.1D'.format(f_id))

        #create a correlation matrix from the roi all time series files
        corr_mat_r = ts_df.corr()
        #the correlations need to be transformed to Fisher z, which is
        #equivalent to the arctanh function.
        corr_mat_z = np.arctanh(corr_mat_r)
        
        #for the first subject, add a correlation matrix of zeros that is the same dimensions as the aal roi-roi matrix
        if i == 0:
            all_corr_mat = np.zeros([corr_mat_z.shape[0], corr_mat_z.shape[1], len(df)])

        #now add the correlation matrix you just created for each subject to the all_corr_mat matrix (3D)
        all_corr_mat[:, :, i] = corr_mat_z
    
    #create the mean correlation matrix (ignore nas - sometime there are some...)
    av_corr_mat = np.nanmean(all_corr_mat, axis=2)
    #create the group covariance matrix (ignore nas - sometime there are some...)
    var_corr_mat = np.nanvar(all_corr_mat, axis=2)
        
    return all_corr_mat, av_corr_mat, var_corr_mat


def split_two_matched_samples(df, motion_thresh, age_l, age_u, n):
    """
    This function takes in a data frame, thresholds it to only include
    participants whose percentage bad frames are less than motion_thresh
    and participants who are between the lower and upper age limits (inclusive),
    then returns two matched samples of size n. The samples are matched on
    age in years, autism diagnosis, gender and scanning site.
    """

    # Start by removing all participants whos data is below a certain
    # motion threshold.
    df_samp_motion = df.loc[df['func_perc_fd'] < motion_thresh, :]

    # Then remove participants who are younger (in years) than age_l and older
    # than age_u. Note that this means people who are age_l and age_u
    # (eg 6 and 10) will be included in the sample.
    df_samp = df_samp_motion.loc[(df_samp_motion['AGE_YRS']>=age_l)
                                    & (df_samp_motion['AGE_YRS']<=age_u), :]

    # Shuffle these remaining participants to ensure you get different sub
    # samples each time you run the code.
    df_samp_rand = df_samp.reindex(np.random.permutation(df_samp.index))

    # Only keep the top 2*n participants.
    df_samp_2n = df_samp_rand.iloc[:2*n, :]

    # Sort these participants according to the sort columns of interest
    sort_column_list = ['DSM_IV_TR', 'DX_GROUP', 'SITE_ID', 'SEX', 'AGE_YRS']
    df_samp_2n_sorted = df_samp_2n.sort_values(by=sort_column_list)

    # Now put all even numbered participants in group A and all odd numbered
    # participants in group B.
    df_grp_A = df_samp_2n_sorted.iloc[::2, :]
    df_grp_B = df_samp_2n_sorted.iloc[1::2, :]

    # Boom! Return these two data frames
    return df_grp_A, df_grp_B



if __name__ == "__main__":
    motion_thresh = np.float(sys.argv[1])
    age_l = np.float(sys.argv[2])
    age_u = np.float(sys.argv[3])
    n = np.int(sys.argv[4])
    n_perms = np.int(sys.argv[5])
    overwrite = np.int(sys.argv[6])

    if overwrite == 1:
        overwrite = True
    elif overwrite == 0:
        overwrite = False
    else:
        print 'invalid option for overwrite, EXITING'
        sys.exit()
        
    abide_motion_wrapper(motion_thresh, age_l, age_u, n, n_perms=n_perms, overwrite=overwrite)


