import argparse
import os
import numpy as np

######################################
#Functions
######################################

def read_fc_data_file(fc_data_file):
    ''' Read an existing functional connectivity data file that also contains labels and demongraphics,
    or create it if it doesn't exist. Returns the data file.
    Args:
        fc_data_file (str): The complete path to the fc data file
    '''
    import pandas as pd
    if not os.path.exists(fc_data_file):
        import create_fc_fisher_z_csv_file as makedata
        subjDF = makedata.read_data()
        fcData = makedata.read_fc_data(subjDF)
        fcData.to_csv(path_or_buf=fc_data_file, index=True)
    else:
        fcData = pd.read_csv(fc_data_file, index_col=0)
    fcData['func_perc_quart'] = pd.qcut(fcData['func_perc_fd'], q=4, labels=False)
    return fcData

def ppc_fc_data(fcData, age_range, motion_threshold,
                labels_col = 'DX_GROUP', strata_cols = ['DX_GROUP', 'func_perc_quart', 'SEX'],
                agecol='AGE_YRS', motioncol='func_perc_fd'):
    ''' Takes an fc file with functional connectivity columns as well as demographics and returns
    strata, labels, and features with imputed values.
    Args:
        fcData (pandas.DataFrame): The fc data file
        age_range (tuple): lower and upper age range for sample
        motion_threshold (int or float): sample will contain rows with func_perc_fd <= motion_threshold
        strata_cols (list of str): columns used to stratify
    '''
    from sklearn.preprocessing import Imputer
    fcData_threshed = fcData.query(agecol + " >= " + str(age_range[0]) + " & " + agecol + "<= " + str(age_range[1]) + " & " + motioncol + " <= " + str(motion_threshold))
    strata = fcData_threshed.groupby(strata_cols).grouper.group_info[0]
    labels = fcData_threshed[labels_col].as_matrix()
    features = fcData_threshed.loc[:,'#2001_#2002':'#9160_#9170']
    features_imputed = Imputer(missing_values='NaN', strategy='mean', axis=0).fit_transform(features)
    return strata, labels, features_imputed

def trainModel(data, labels, strata, modelDir = None, fname_prefix = None, classifier = 'svc',  cv = True, cvmethod = 'sss', n_iter = 10, k = 10, sparse = True, saveData = True, n_jobs=1):
    '''Applies classifier to predict labels from data, stratified by strata, and returns the resulting model.
    Optionally saves the model and coefficients.
    Args:
        data (numpy.ndarray): features to use in prediction
        labels (numpy.ndarray): labels to predict
        strata (numpy.ndarray): labels to use for stratification
        classifier (str): classifier to use. currently only svc is implemented
        modelDir (str): where to save model and csv files
        fname_prefix (str): what to attach to the beginning of the filename
        cv (bool): implement cross validation? currently this must be true
        cvmethod (str): cross validation method, 'sss' for StratifiedShuffleSplit or 'skf' for StratifiedKFold.
        n_iter (int): number of times to iterate the StratifiedShuffleSplit; default true
        k (int): if classifier is StratifiedKFold, number of folds; default true
        sparse (bool): whether to use l1 (sparse) regularization or l2; default True
        saveData (bool): save the results to model directory? default True
        n_jobs (int): number of jobs to pass to cv
    '''
    if sparse:
        penalty = 'l1'
    else:
        penalty = 'l2'
    if classifier == 'svc':
        from sklearn.svm import LinearSVC
        algorithm = LinearSVC(penalty = penalty)
        if penalty == 'l1':
            algorithm.set_params(dual=False)
    if cv:
        from sklearn.grid_search import GridSearchCV
        paramsToSearch = []
        paramsToSearch.append({'C': [.001,.005,.01,.1,1,10]})
        if cvmethod == 'sss':
            from sklearn.cross_validation import StratifiedShuffleSplit
            cvalgorithm = StratifiedShuffleSplit(strata, n_iter = n_iter, test_size = .3)
        if cvmethod == 'skf':
            from sklearn.cross_validation import StratifiedKFold
            cvalgorithm = StratifiedKFold(strata, n_folds = n_folds, shuffle = True)
        clf=[]
        clf = GridSearchCV(algorithm,
                           paramsToSearch,
                           cv=cvalgorithm,
                           n_jobs=n_jobs)
    else:
        #Defaults and train model
        clf = algorithm
    clf.fit(data, labels)

    #Get training accuracy
    from sklearn.metrics import accuracy_score
    trainingPredictions = clf.predict(data)
    accuracy = accuracy_score(trainingPredictions, labels)
    print "Training accuracy: %f" % accuracy

    if cv:
        #Extract tuned model weights
        modelWeights = clf.best_estimator_.coef_[0]
        modelIntercept = clf.best_estimator_.intercept_
    else:
        #Extract deafult model weights
        modelWeights = clf.coef_[0]
        modelIntercept = clf.intercept_

    if saveData:
        if (not modelDir) | (not fname_prefix):
            raise TypeError('Model dir or file name not specified')
        print "Saving model weights, training accuracy, and model"
        from sklearn.externals import joblib
        #Write intercept + model weights to csv
        if not os.path.exists(modelDir):
            print ("{} does not exist; creating ...".format(modelDir))
            os.makedirs(modelDir)
        fileName = os.path.join(modelDir, fname_prefix)
        print ("Writing data to {}*".format(fileName))
        np.savetxt(fileName + '_TrainLabelFreq.csv',np.unique(labels, return_counts=True), delimiter=',', newline=os.linesep)
        np.savetxt(fileName + '_Weights.csv',np.concatenate([modelIntercept,modelWeights]), delimiter=',', newline=os.linesep)
        np.savetxt(fileName + '_TrainAcc.csv',np.array([accuracy]), delimiter=',',newline=os.linesep)
        joblib.dump(clf, fileName + '_Model.pkl')

    return (clf)

def testModel(data, labels, clf = None, modelDir = None, fname_prefix = None, outputDir = None, saveData=True):

    ''' Test a linear classifier by loading a fitted model and returning predictions on given data.
    Args:
        data (ndarray): A data matrix organized as nsamples x nfeatures
        labels (ndarray): A 1d labels array same length as nsamples
        clf (sklearn fit object): If not specified, fucntion will try to load using modelDir and fname_prefix
        modelDir (str): directory from which to load pickled model files
        fname_prefix (str): filename prefix used for model files
        outDir (str): directory to write csv file with testing accuracy and predictions
        saveData (bool; optional): whether to actually save csv or just return model object;
            default True
    '''

    from sklearn.externals import joblib
    from sklearn.metrics import accuracy_score

    if not clf:
        if (not modelDir) | (not fname_prefix):
            raise TypeError('No clf provided and Model dir or file name not specified')
        modelPath = os.path.join(modelDir, fname_prefix)
        #If model doesn't exist use csv with coefs - TODO
        clf = joblib.load(modelPath + '_Model.pkl')
    predictions = clf.predict(data)

    #Compute accuracy on test data
    accuracy = accuracy_score(predictions,labels)
    print "Testing accuracy: %f" % accuracy

    if saveData:
        from sklearn.externals import joblib
        if (not outputDir) | (not fname_prefix):
            raise TypeError('Output dir or file name not specified')
        if not os.path.exists(outputDir):
            print ("{} does not exist; creating ...".format(outputDir))
            os.makedirs(outputDir)
        outPath = os.path.join(outputDir, fname_prefix)
        print "Saving test accuracy and predictions to {}*".format(outPath)
        np.savetxt(outPath + '_TestLabelFreq.csv',np.unique(labels, return_counts=True), delimiter=',', newline=os.linesep)
        #Save accuracy
        np.savetxt(outPath + '_TestAcc.csv', np.array([accuracy]), delimiter=',',newline=os.linesep)
        #Save predictions
        np.savetxt(outPath + '_Predictions.csv',predictions, delimiter=',',newline=os.linesep)

    return accuracy 

######################################
######################################

# Get arguments
parser = argparse.ArgumentParser(description='ABIDE Prediction Accuracy Test of Subject Inlcusion Motion Thresholds')
parser.add_argument('--fc_file', help='File containing the functional connectivity and'
    'demographic information for the analysis that will be run. This is a CSV file.', required=True)
parser.add_argument('--output_dir', help='Directory to contain output i.e. model weights and  model details',required=True)
parser.add_argument('--model_dir', help='Directory to store model objects if training and load model objects if necessary.',required=True)
parser.add_argument('--mt', help='Motion threshold. Participants with greater than this percentage of bad volumes will be excluded from analyses.',required=True)
parser.add_argument('--N', help='Sample size for training sample, and testing sample.',required=True)
parser.add_argument('--cvmethod', help='Type of cross validation to use; one of: sss OR skf for stratified shuffle split or stratified k-fold, respectively.', required=True)
parser.add_argument('--agelower',default=6, help='Lower age limit; defaults to 6.')
parser.add_argument('--ageupper',default=18, help='Upper age limit; defaults to 18.')
#parser.add_argument('--model', help='Type of classifier to use; one of: svm OR logistic', required=True) #not yet ready
#parser.add_argument('--train', action='store_true') # in the future, it may be possible to train or test only
#parser.add_argument('--test', action='store_true')
#parser.add_argument('--noCV',action='store_false',default=True, help='Indicate whether CV should be NOT used to tune hyperparameters and use sklearn defaults instead') # not implemented yet
parser.add_argument('--oos_iter', default=10, help='How many out-of-sample prediction accuracy tests should be run (each one incurs a cross-validated classifier estimation cost); defaults to 10')
parser.add_argument('--sss_iter',default=10, help='Indicate number of CV stratified shuffle splits to use during hyper-parameter tuning; defaults to 10')
parser.add_argument('--k',default=3, help='Indicate number of CV folds to use during hyper-parameter tuning; defaults to 3')
parser.add_argument('--non_sparse',action='store_false',default=True, help='Indicate whether a non-sparse model should be fit using L2 regularization; defaults to L1')
parser.add_argument('--nosave',action='store_false',default=True, help='Indicate whether models should be estimated but no files should be written; mostly for debugging')

# get the command line arguments
args = parser.parse_args()

# Check for correct and sufficient arguments
#if args.train is None and args.test is None:
#    parser.error('Enter flag for data: --train or --test')

# Check for phenofile
if not args.fc_file:
    parser.error('Need FC fule file with demographics')
else:
    fc_data_file = os.path.abspath(args.fc_file)

# output directory
outputDir=os.path.abspath(args.output_dir)

# model directory
modelDir=os.path.abspath(args.model_dir)

if not args.mt:
    parser.error('Need motion threshold')
else:
    motion_threshold = int(args.mt)

if not args.N:
    parser.error('Need sample size')
else:
    sample_size = int(args.N)

if not args.cvmethod:
    parser.error('Must specify one of the following cv methods: sss or skf')
else:
    cvmethod=args.cvmethod

if not (args.agelower & args.ageupper):
    parser.error('Need lower and upper age limit')
else:
    age_range = (float(args.agelower), float(args.ageupper))

classifier='svc' #only option, for now

if not args.oos_iter:
    parser.error('Must specify number of out-of-sample iterations')
else:
    oos_iter=int(args.oos_iter)

if not args.sss_iter:
    parser.error('Must specify number of stratified shuffle split iterations')
else:
    sss_n_iter=int(args.sss_iter)

if not args.k:
    parser.error('Must specify number of folds')
else:
    skf_n_folds=int(args.k)

#set filename prefix
fname_prefix = "{}_{}_mt{}_n{}".format(cvmethod, classifier, motion_threshold, sample_size)

#read the fc_data_file
fcData = read_fc_data_file(fc_data_file)

#preprocess the data file
strata, labels, features = ppc_fc_data(fcData, age_range, motion_threshold)

#
from sklearn.cross_validation import StratifiedShuffleSplit
sss = StratifiedShuffleSplit(strata, n_iter = oos_iter, test_size = sample_size, train_size = sample_size)

print("Running {} iterations of {} cv'd {} classification\n".format(oos_iter, cvmethod, classifier) +
      "Each N = {}, Motion thresh = {}".format(sample_size, motion_threshold))

for i, (train_index, test_index) in enumerate(sss):
    train_features, train_labels = features[train_index, :], labels[train_index]
    test_features, test_labels = features[test_index, :], labels[test_index]
    ifname_prefix = fname_prefix + '_i{:03d}'.format(i)
    aCLF = trainModel(train_features, train_labels, train_labels,
                      modelDir=modelDir, fname_prefix=ifname_prefix,
                      classifier = classifier,
                      cv = True, cvmethod = cvmethod,
                      n_iter = sss_n_iter, k = skf_n_folds,
                      sparse = True, saveData = True, n_jobs=4)
    accuracy = testModel(test_features, test_labels, clf = aCLF,
                         fname_prefix = ifname_prefix,
                         outputDir = outputDir, saveData=True)


