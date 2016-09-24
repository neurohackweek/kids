import numpy as np
import os
import pandas as pd
import sys

def create_fc_features(file_id):
    aTable = pd.read_table('DATA/%s_rois_aal.1D' % file_id)
    corr_df_r = aTable.corr(method='pearson')
    corr_mat_r = corr_df_r.as_matrix()
    upperTriInds = np.triu_indices_from(corr_mat_r, k=1)
    corr_vector_r = corr_mat_r[upperTriInds]
    rownames = corr_df_r.index
    colnames = corr_df_r.columns
    corr_vector_names = []
    for row, col in zip(upperTriInds[0], upperTriInds[1]):
        corr_vector_names += [str(rownames[row]) + "_" + str(colnames[col])]
    newSeries = pd.Series(data=corr_vector_r,
                         index=corr_vector_names)

    return newSeries

def read_data():
    behav_data_f = '../../Phenotypic_V1_0b_preprocessed1.csv'

    df = pd.read_csv(behav_data_f)
    df = df.loc[df['func_perc_fd'].notnull(), :]
    df = df.loc[df['FILE_ID']!='no_filename', :]
    df['AGE_YRS'] = np.floor(df['AGE_AT_SCAN'])

    return df

def read_fc_data(df):
    fcData = df[['subject', 'func_perc_fd', 'AGE_YRS', 'SEX', 'DX_GROUP']].merge(
        np.arctanh(df['FILE_ID'].apply(create_fc_features)), 
        left_index=True, 
        right_index=True)
    
    return fcData

if __name__ == "__main__":
    subjDF = read_data()
    fcData = read_fc_data(subjDF)
    
    fcData.to_csv(path_or_buf='./abide_fc_data_fisher_z.csv')