#!/usr/bin/env python

import numpy as np
import os
import pandas as pd


def calc_rsq(av_corr_mat_A, av_corr_mat_B):
    """
    This function takes in two average correlation matrices and calculates the R squared between them. 
    It returns one R squared value.
    
    From wikipedia: https://en.wikipedia.org/wiki/Coefficient_of_determination
    
    Rsq = 1 - (SSres / SStot)
    
    SSres is calculated as the sum of square errors (where the error
    is the difference between x and y).
    
    SStot is calculated as the total sum of squares in y.
    """
    # Get the data we need
    # Find indices of top half of covariance matrix (don't include diaganal)
    inds = np.triu_indices_from(av_corr_mat_B, k=1)
    #x = the top half of covariance matrix A put into one row
    x = av_corr_mat_A[inds]
    #x = the top half of covariance matrix B put into one row
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