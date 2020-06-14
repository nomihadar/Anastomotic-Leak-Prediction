
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


if __name__ == "__main__":
    
    #read input file  
    input_path = os.path.join(DPATH_DATA, INPUT_FILE) 
    df = pd.read_csv(input_path)
    print(df.shape)

    #Drop duplicate rows 
    prev_num_rows = df.shape[0]
    df.drop_duplicates(inplace=True)
    print("Num duplicate rows:", prev_num_rows - df.shape[0])

    #Drop rows where patient id is null
    null_pid = df[df["pid"].isna()]
    print(null_pid.head())
    df = df[df["pid"].notna()]
    print("Num rows with missing patient id:", null_pid.shape[0])

    #******** Missing values
    print(df.info())
    #drop columns with all NaN's.
    # There are columns with few non-nan values.
    df = df.dropna(axis=1, how='all')
    print(df.shape)

    #Print percentage of missing values in each column.
    percent_missing = df.isna().mean().round(5).mul(100).rename_axis("percent missing values")
    print(percent_missing)

    #******* Drop irrelevant columns. Num left columns: 18. 
    cols_to_remove = ["rowId", "id", "altPid", "bed", "cancelled", "converted", \
        "messageId", "parentId", "tValue", "transferrable", "careGiver", "Time_Stamp"]
    df.drop(columns=cols_to_remove, inplace=True, errors='ignore')
    print(df.info())

    #Reorder columns
    cols_ordered = ["pid", "admissionId", "eventName", \
                "eventStartDate", "eventEndDate",  \
                "bValue", "dValue", "iValue", "sValue", \
                "eventDesc", "unitOfMeasure", \
                "orderNumber", "organismId", \
                "eventCode", "eventCodeOrg", \
                "eventType", "eventTypeOrg", "sourceName"]

    df = df[cols_ordered]

    print("Resulted file shape:", df.shape)

    #write output
    output_path = os.path.join(DPATH_DATA, OUT_FILE)
    if not os.path.exists(output_path):
        df.to_csv(output_path, index=False)

