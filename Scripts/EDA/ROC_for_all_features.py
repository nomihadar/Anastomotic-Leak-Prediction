
import sys, os
sys.path.append(os.path.dirname(sys.path[0])) #to change to environment 
from utils.constants import *

import argparse 
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score


def youdens_j(fpr, tpr):

    '''
    Find the optimal threshold by Youden's J method, 
    which is the following statistic:
    J = sensitivity + specificity - 1 

    Arguments:
    fpr -- list of true positive rates 
    tpr -- list of true positive rates 

    Returns: 
    optimal_idx -- optimal index of threshold 
    
    '''
    optimal_idx = np.argmax(tpr - fpr)
    

    return optimal_idx

def compute_ROC_per_feature(x, y):

    FEATURE = 'feature' #name of feature 
    N  = 'n_patients' #number of patients having feature 
    TPR = 'sensitivity' #true positive rate (sensitivity) for optimal threshold 
    FPR = '1−specificity' #false positive rate (1 − specificity) for optimal threshold  
    AUC = 'AUC' #AUC score 
    BEST_THRES_IDX = 'optimal_threshold idx'
    BEST_THRES_VALUE = 'optimal_threshold value'

    d = {FEATURE : [], N : [], TPR : [], FPR : [], AUC : [], 
            BEST_THRES_IDX : []}
    

    #for each column (feature) compute sensitivity, specificity, and AUC
    for col in x.columns:
        #get feature values (remove missing rows)
        feature = x[col].dropna()
        y_true = y[x[col].notna()]


        #get false/true positive rates, and thresholds.
        fpr, tpr, thresholds = roc_curve(y_true, feature, pos_label=1)
        #compute area under curve (AUC)
        auc = roc_auc_score(y_true, feature)
        #compute the optimal threshold 
        optimal_idx = youdens_j(fpr, tpr)
        optimal_threshold = thresholds[optimal_idx]

        #add to dictionary 
        d[FEATURE].append(col)
        d[N].append(len(feature))
        d[TPR].append(tpr[optimal_idx])
        d[FPR].append(fpr[optimal_idx])
        d[AUC].append(auc)
        d[BEST_THRES_IDX].append(optimal_idx)


    df = pd.DataFrame(d)

    return df

def matrix_info(matrix):
    print()
    print("matrix size:", matrix.shape)
    types = pd.Series(matrix.dtypes).value_counts()
    print("matrix types: \n", types)
    print()

if __name__ == "__main__":
    
    #get path of features matrix
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', type=str, help='input name of features-matrix file')
    #parser.add_argument('-out', type=str, help='output name of result file')
    args = parser.parse_args()
    
    #concatenate paths
    input_path = os.path.join(DATA_PATH, args.file)
    #output_path = os.path.join(P, args.file)

    #read features matrix 
    matrix = pd.read_excel(input_path, header=MATRIX_HEADER, index_col=0)

    #print matrix info
    matrix_info(matrix)

    #get y 
    y = matrix.iloc[:,Y_COL_IDX]

    #get x, and get numeric features only
    x = df.drop(columns=matrix.columns[Y_COL_IDX])._get_numeric_data()

    #compute ROC
    df = compute_ROC_per_feature(x, y)

    #write output 
    df.to_csv(output_path)

