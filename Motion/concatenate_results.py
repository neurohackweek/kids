import pandas as pd
from glob import glob 
#,motion_thresh,age_l,age_u,n,med_rsq,CI_95,med_icc,CI_95_icc
columns = [ 'motion_thresh', 'med_rsq', 'CI_95', 'med_icc', 'CI_95_icc', 'n', 'age_l', 'age_u' ]
results_df = pd.DataFrame(columns = columns)

for f in glob('RESULTS/*csv'):
   temp_df = pd.read_csv(f, index_col=0)
   results_df = results_df.append(temp_df)
   
results_df.to_csv('RESULTS/SummaryRsqs.csv', index=None, columns=columns)
