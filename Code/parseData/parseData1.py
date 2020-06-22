
'''
- Drop duplicate rows.
- Drop rows where patient id is null.
- Drop empty columns.
- Drop irrlevant columns.
'''

import sys, os
sys.path.append(os.path.dirname(sys.path[0])) #to change to environment 
from utils.constants import *
 
import pandas as pd

#files names 
INPUT_FILE = "data0.csv"
OUT_FILE = "data1.csv"

def reorderColumns(df):
    cols_ordered = ["pid", "admissionId", "eventName", \
        "eventStartDate", "eventEndDate",  \
        "bValue", "dValue", "iValue", "sValue", \
        "eventDesc", "unitOfMeasure", \
        "orderNumber", "organismId", \
        "eventCode", "eventCodeOrg", \
        "eventType", "eventTypeOrg", "sourceName"]

    df = df[cols_ordered]

def dropColumns(df):

    #drop columns with all NaN's.
    # There are columns with few non-nan values.
    print("\nnum rows where all values are null:", \
        df.isna().all(axis=0).sum(), "\n")
    df.dropna(axis=1, how='all', inplace=True)

    #Drop irrelevant columns
    cols_to_drop = ["rowId", "id", "altPid", "bed", \
        "cancelled", "converted", \
        "messageId", "parentId", "tValue", \
        "transferrable", "careGiver", "Time_Stamp"]
    
    print("num irrelevant columnas:", len(cols_to_drop), "\n") 

    df.drop(columns=cols_to_drop, inplace=True)

def dropRows(df):

    #drop rows with all NaN's.
    print("num rows where all values are null:", df.isna().all(axis=1).sum())
    df.dropna(axis=0, how='all', inplace=True)

    #drop duplicate rows 
    print("\nNum duplicate rows:", df.duplicated().sum())
    df.drop_duplicates(inplace=True)
    
    #drop rows where patient id is null
    print("\nNum rows with missing patient id:", df["pid"].isna().sum(), "\n")
    
    #reset index 
    df.reset_index(drop=True, inplace=True)

def sortRows(df):

    #parse date of start/end event
    df['eventStartDate'] = pd.to_datetime(df['eventStartDate'], format='%Y-%m-%d')
    df['eventEndDate'] = pd.to_datetime(df['eventEndDate'], format='%Y-%m-%d')
    #sort
    df.sort_values(["pid", "eventStartDate"], inplace=True)


if __name__ == "__main__":
    
    #read input file  
    input_path = os.path.join(DPATH_DATA, INPUT_FILE) 
    df = pd.read_csv(input_path)
    print("input file shape:", df.shape)

    #print info
    print("\n\nINFO:\n\n", df.info())

    #print percentage of missing values in each column.
    percent_missing = df.isna().mean().round(5).mul(100)\
        .to_frame("% missing values")
    print("\n", percent_missing)

    #sort rows
    sortRows(df)

    #drop null and irrelevant columns. Num left columns: 18. 
    dropColumns(df)

    #drop rows 
    dropRows(df)
   
    #print info
    print("\n\nINFO:\n\n", df.info())
   
    #reorder columns
    reorderColumns(df)

    #print resulted shape
    print("Resulted file shape:", df.shape)

    #write output
    output_path = os.path.join(DPATH_DATA, OUT_FILE)
    if not os.path.exists(output_path):
        df.to_csv(output_path, index=False)

