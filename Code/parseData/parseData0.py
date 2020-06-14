
'''
Merge all events files into one file.
Add columns headers.
'''

import sys, os
sys.path.append(os.path.dirname(sys.path[0])) #to change to environment 
from utils.constants import *

import argparse 
import pandas as pd


#num files
NUM_FILES = 10

#files names 
HEADERS_FILE = "eventsHeader.csv"
EVENTS_FILE = "Events{}.csv"
OUT_FILE = "data0.csv"

def get_headers():

    headers_path = os.path.join(DPATH_SOURCES, HEADERS_FILE) 
    with open(headers_path, 'r') as f:
        headers = f.read().strip().split('|')
        print("num headers:", len(headers))
        print(headers)
    
    return headers

def mergeFiles(headers):

    #path of events files 
    paths = [os.path.join(DPATH_SOURCES, EVENTS_FILE.format(i)) \
        for i in range(NUM_FILES)]
    
    #read each file into a data frame
    frames = [pd.read_csv(file, sep='|', encoding='cp1255', names=headers) \
        for file in paths]

    #get types of each data frame, to verify they can be combined into one file
    frames_types = [df.dtypes for df in frames]

    #Explore types
    # Datatypes of columns are identical along files, 
    # except of column "tValue" which is of type "float64" in files 1-9, and "object" in file 0
    types_df = pd.concat(frames_types, axis=1, ignore_index=True).T
    types_df.index = ["file_{}".format(i) for i in range(NUM_FILES)]
    print("types:", types_df)

    mixed = types_df.nunique(axis=0).ne(1)
    print("Colums where types are mixed:", mixed.loc[mixed].index.values)

    #The "object" values in column 'tValue', file 0, are dates, 
    # while values of column 'tValue' in rest files are null.
    print(df_file0['tValue'].dropna())
    df_file1 = frames[1]
    print()
    print(df_file1['tValue'].dropna())

    #Combine events file into one file
    #combine files into one data frame
    df = pd.concat(frames, axis=0, ignore_index=True)

    print("Merged file shape:", df.shape)

    return df


if __name__ == "__main__":
    
    #get path of features matrix
    parser = argparse.ArgumentParser()
    parser.add_argument('-out', type=str, help='output name of result file')
    args = parser.parse_args()

    #create output path 
    if args.out:
        output_path = os.path.join(DPATH_DATA, args.out)
    else:
        output_path = os.path.join(DPATH_DATA, OUT_FILE)

    #get headers
    headers = get_headers()

    #read one file first 
    file0 = os.path.join(DPATH_SOURCES, EVENTS_FILE.format(0))
    df_file0 = pd.read_csv(file0, sep='|', encoding='cp1255', names=headers)
    print("\n\n", "file0 shape:", df_file0.shape, "\n")
    print(df_file0.info(), "\n")
    print(df_file0.head())

    #merge files into one dataframe
    df = mergeFiles(headers)
   
    #write output
    df.to_csv(output_path)

