
import sys, os
sys.path.append(os.path.dirname(sys.path[0])) #to change to environment 
from utils.constants import *
from utils.defs_functions import getHebrewWords

import argparse 
import pandas as pd


#files names 
INPUT_FILE_1 = "anonymous_080620_DA.xlsx"
INPUT_FILE_2 = "anonymousFull.xlsx"

DICT_FILE = "dictionary_anonymous_file.xlsx"

OUT_FILE_1 = "anonymous_080620_DA_translated.xlsx"
OUT_FILE_2 = "anonymousFull_translated.xlsx"

def createDictionary(df1, df2, dict_path):
    #extract the Hebrew words, and create a dictionary file
    # (add translations manually)

    #get the Hebrew words in the data frame
    df1_cells = getHebrewWords(df1) 
    df1_cols = getHebrewWords(list(df1.columns))
    df2_cols = getHebrewWords(list(df2.columns))
    df_hebrew = pd.concat([df1_cells, df1_cols, df2_cols])

    df_hebrew.to_excel(dict_path, index=False, header=False) #uncomment after creating dictionary


def translate(df, dict_path):

    #read Hebrew-English dictionary (manually created)
    dictionary = pd.read_excel(dict_path, header=None, index_col=0).to_dict()[1]
    dictionary

    #translate cells
    df.replace(dictionary, inplace=True)

    #translate headers
    headers = pd.Series(df.columns).replace(dictionary)
    df.columns = pd.Index(headers.str.title())


if __name__ == "__main__":
    
    #read input files
    input_path = os.path.join(DPATH_SOURCES, INPUT_FILE_1) 
    df1 = pd.read_excel(input_path)

    input_path = os.path.join(DPATH_SOURCES, INPUT_FILE_2) 
    df2 = pd.read_excel(input_path)
    
    print("files sizes:", df1.shape, df2.shape)
    print(df1.head)
    print(df2.head)

    #dict path
    dict_path = os.path.join(DPATH_ANONYMOUS, DICT_FILE) 

    #if dictionary does not exist yet (first execute) - create one
    if not os.path.exists(dict_path):
        createDictionary(df1, df2, dict_path)

    #translate 
    translate(df1, dict_path)
    translate(df2, dict_path)

    #save translated files
    output_path = os.path.join(DPATH_ANONYMOUS, OUT_FILE_1) 
    with pd.ExcelWriter(output_path, datetime_format='DD/MM/YYYY') as writer:
        df1.to_excel(writer, index =False)

    output_path = os.path.join(DPATH_ANONYMOUS, OUT_FILE_2) 
    with pd.ExcelWriter(output_path, datetime_format='DD/MM/YYYY') as writer:
        df2.to_excel(writer, index =False)




    






   

