
# num_iter=3
# method_array=("svm" "logistic")
def get_qsub_file(num_iter=3, methods=['svm', 'logistic']):
    head = '''#!/bin/bash
## SGE batch file
#$ -S /bin/bash
#$ -N train_and_test
#$ -t 1-12
#$ -V
#$ -cwd

num_itr=%s
declare -a method_array=%s
''' % (num_iter, '(%s)' % ' '.join(['"%s"' % tmp for tmp in methods]))
    tail = '''
num_set=2
num_method=${#method_array[@]}

echo SGE_TASK_ID=$SGE_TASK_ID

let index=$SGE_TASK_ID-1
let num_itr_set=$num_itr*$num_set
let method_index=$index/$num_itr_set+1
let itr_number=($index%$num_itr_set)/$num_set+1
let set_number=$index%$num_set+1

method=${method_array[$method_index-1]}
let test_set_number=3-$set_number

pgm="python runClassifier.py"
input_dir=../input/reho
output_base=../output/out
output_dir=${output_base}/${method}_set${set_number}_iteration${itr_number}
mask=../input/MNI3mm.nii.gz
csv_file="${output_base}/set${set_number}_iteration${itr_number}.csv"
test_csv_file="${output_base}/set${test_set_number}_iteration${itr_number}.csv"

echo $method, itr $itr_number, set $set_number, testset $test_set_number, csv $csv_file, testcsv $test_csv_file

cd /home/ubuntu/kids/script
#. /home/ubuntu/.bashrc

source activate cpac

#pip install -q scikit-learn
#conda install -q -y scikit-learn
#pip install nilearn

echo
echo mkdir -p ${output_dir}
mkdir -p ${output_dir}

echo
echo ${pgm} --pheno_file ${csv_file} --input_dir ${input_dir} --output_dir ${output_dir} --train --mask ${mask} --classfr ${method}
${pgm} --pheno_file ${csv_file} --input_dir ${input_dir} --output_dir ${output_dir} --train --mask ${mask} --model ${method}    --model_dir ${output_dir}
echo Done training

echo
echo ${pgm} --pheno_file ${test_csv_file} --input_dir ${input_dir} --output_dir ${output_dir} --test --mask ${mask} --model ${method}    --model_dir ${output_dir}
${pgm} --pheno_file ${test_csv_file} --input_dir ${input_dir} --output_dir ${output_dir} --test --mask ${mask} --model ${method}    --model_dir ${output_dir}
echo Done testing
'''
    return head + tail

