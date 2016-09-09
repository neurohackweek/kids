#!/usr/bin/env python

import numpy as np
import os
import pandas as pd


def make_group_corr_mat(df):
    """
    This function reads in each subject's aal roi time series files and creates roi-roi correlation matrices
    for each subject and then sums them all together. The final output is a 3d matrix of all subjects 
    roi-roi correlations, a mean roi-roi correlation matrix and a roi-roi covariance matrix.
    """

    # for each subject do the following
    
    for i, (sub, f_id) in enumerate(df[['SUB_ID', 'FILE_ID']].values):
        
        #read each subjects aal roi time series files
        ts_df = pd.read_table('../DATA/{}_rois_aal.1D'.format(f_id))

        #create a correlation matrix from the roi all time series files
        corr_mat = ts_df.corr()
        
        #for the first subject, add a correlation matrix of zeros that is the same dimensions as the aal roi-roi matrix
        if i == 0:
            all_corr_mat = np.zeros([corr_mat.shape[0], corr_mat.shape[1], len(df)])

        #now add the correlation matrix you just created for each subject to the all_corr_mat matrix (3D)
        all_corr_mat[:, :, i] = corr_mat
    
    #create the mean correlation matrix (ignore nas - sometime there are some...)
    av_corr_mat = np.nanmean(all_corr_mat, axis=2)
    #create the group covariance matrix (ignore nas - sometime there are some...)
    var_corr_mat = np.nanvar(all_corr_mat, axis=2)
        
    return all_corr_mat, av_corr_mat, var_corr_mat