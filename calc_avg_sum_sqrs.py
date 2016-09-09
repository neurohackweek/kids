#!/usr/bin/env python

import numpy as np
import os
import pandas as pd


def calc_avg_sum_sqrs(av_corr_mat_A, av_corr_mat_B):
    
    """
    This function takes in an average correlation matrix for group A and group B (created with make_group_corr_mat.py)
    and calculates the average root mean squared of the fit between the two samples roi-roi correlations. 
    """
    
    #find indices of top half of covariance matrix (don't include diaganal)
    inds = np.triu_indices_from(av_corr_mat_B, k=1)
    
    #x = the top half of covariance matrix a put into one row
    x = av_corr_mat_A[inds]
    
    #y = the top half of covariance matrix a put into one row
    y = av_corr_mat_B[inds]
    
    
    res = y - x
    res_sq = res**2
    av_sum_sqrs = np.sum(res_sq)/len(x)
    return av_sum_sqrs
    