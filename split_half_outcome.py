#!/usr/bin/env python

import numpy as np
import os
import pandas as pd


def split_half_outcome(df, motion_thesh, age_l, age_u, n, n_perms=100):
    
    """
    This function returns the R squared of how each parameter affects split-half reliability!
    It takes in a dataframe, motion threshold, an age upper limit(age_u) an age lower limit (age_l), sample size (n),
    and number of permutations (n_perms, currently hard coded at 100). This function essentially splits a data frame 
    into two matched samples (split_two_matched_samples.py), then creates mean roi-roi correlation matrices per sample 
    (make_group_corr_mat.py) and then calculates the R squared (calc_rsq.py) between the two samples'
    correlation matrices and returns all the permuation coefficients of determinations in a dataframe.
    """
    
    #set up data frame of average R squared to fill up later
    av_sum_sqrs_list = []
    
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
