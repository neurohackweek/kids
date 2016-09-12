# ML

Classifier Design: HoJin, Swati, Ann, Eshin
https://github.com/preprocessed-connectomes-project/abide

Available
fMRI: 3D volume per subject, redo
Structure: Freesurfer (Desikan Killany)
Demographic data: Phenotypic_V1_0b_preprocessed.csv: (ABIDE_LEGEND_v1.02.pdf)
73 potential features

Steps
Look at run.py
Download data - works, downloaded reho data only from PITT for starters
python download_abide_preproc.py -d reho -p cpac -s filtnoglobal -o reho -t PITT

Mini Project 1:
Read csv file of phenotypic information - removed QA measures from ABIDE, will use from our group
Reduce data based on csv (remove not research reliable data)
SEX (474M-65F/474M-99F), AGE, DX, FIQ values are available for most subjects ~ 900, otherwise dataset reduces to 200
Do PCA or some data reduction - not needed

Simple explanation of ReHo: http://nro.sagepub.com/content/early/2015/10/28/1073858415595004.full

Mini Project 1 apply to
 cortical measures
Mini Project 1 apply to
 fMRI voxelwise data 

Mini Project 2: 
Combine reduced features (phenotypic, structural, fMRI)
Run Miniproject 1 of the combined features

Mini Project 3:
Classifier: What kind? 

Extra
Mini Project 4:
Compare with Deep Learning algorithm on reduced datasets