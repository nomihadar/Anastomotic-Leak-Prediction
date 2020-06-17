
'''
Get list of patients codes.
'''

import sys, os
sys.path.append(os.path.dirname(sys.path[0])) #to change to environment 
from utils.constants import *

import pandas as pd

#files names 
INPUT_FILE = "data0.csv"
OUT_FILE = "patientsList.xlsx"


if __name__ == "__main__":
    
    #read input file  
    input_path = os.path.join(DPATH_DATA, INPUT_FILE) 
    df = pd.read_csv(input_path)
    print("input file shape:", df.shape)

    #get patients code
    patients = df['pid'].drop_duplicates().dropna()
    print("patients:", patients.shape)

    #write output
    output_path = os.path.join(DPATH_ANONYMOUS, OUT_FILE)
    if not os.path.exists(output_path):
        patients.to_excel(output_path, index=False)

