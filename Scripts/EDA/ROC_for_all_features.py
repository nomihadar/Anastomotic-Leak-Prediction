
import sys, os
import argparse
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(sys.path[0]))
#sys.path.insert(1, '..\Scripts')
from defs.defs_paths import *
from sklearn.metrics import roc_curve, roc_auc_score


def youdens_j(fpr, tpr, thresholds):

    '''
    Find the optimal threshold 
    Youden's J statistic is:
    J = sensitivity + specificity - 1 
    
    '''
    optimal_idx = np.argmax(tpr - fpr)
    optimal_threshold = thresholds[optimal_idx]
       
    return optimal_threshold

def compute_ROC_per_feature(matrix):

    SENS = 'sensitivity'
    SPEC = '1 − specificity'
    AUC = 'AUC'
    BEST_THRES = 'optimal threshold'

    d = {SENS : [], SPEC : [], AUC : [], BEST_THRES : []}
    
    #get features
    features = []

    #get y true 
    y_true = matrix

    #for each feature compute sensitivity, specificity, and AUC
    for feature in features:
        #get false/true positive rates, and thresholds.
        fpr, tpr, thresholds = roc_curve(y_true, feature, pos_label=1)
        #compute area under curve (AUC)
        auc = roc_auc_score(y_true, feature)

        optimal_threshold = youdens_j(fpr, tpr, thresholds)

        #add to dictionary 
        d[SENS].append(tpr)
        d[SPEC].append(fpr)
        d[AUC].append(auc)
        d[BEST_THRES].append(optimal_threshold)


    df = pd.DataFrame(d)

    return df



if __name__ == "__main__":
    
    #get path of features matrix
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', type=str, help='file name of features matrix file')
    args = parser.parse_args()
    
    full_path = os.path.join(DATA_PATH, args.file)

    #read features matrix 
    matrix = pd.read_excel(full_path)

    #compute
    df = compute_ROC_per_feature(matrix)

    #write output 
    #df.to_csv()

