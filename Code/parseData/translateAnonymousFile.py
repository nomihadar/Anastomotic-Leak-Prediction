
import sys, os
sys.path.append(os.path.dirname(sys.path[0])) #to change to environment 
from utils.constants import *
from utils.defs_functions import getHebrewWords

import argparse 
import pandas as pd

DICT_FILE = "dictionary_anonymous_file.xlsx"

def createDictionary(df, dict_path):
    #extract the Hebrew words, and create a dictionary file
    # (add translations manually)

    #get the Hebrew words in the data frame
    df_hebrew_cells = getHebrewWords(df) 
    df_hebrew_cols = pd.DataFrame({"words" : list(df.columns[1:11])})
    df_hebrew = pd.concat([df_hebrew_cells, df_hebrew_cols])

    df_hebrew.to_excel(dict_path, index=False, header=False) #uncomment after creating dictionary


def translate(df, dict_path):

    #read Hebrew-English dictionary (manually created)
    dictionary = pd.read_excel(dict_path, header=None, index_col=0).to_dict()[1]
    dictionary

    #translate 
    df.replace(dictionary, inplace=True)

    #translate headers
    headers = df.columns
    new_headers = [dictionary[header] 
                    if header in dictionary 
                    else header.title() 
                    for header in headers]
    df.columns = new_headers


if __name__ == "__main__":
    
    #get names of files
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', type=str, help='input name of anonymous file')
    parser.add_argument('-out', type=str, help='output name of translated-anonymous file')
    args = parser.parse_args()
    
    #concatenate paths
    input_path = os.path.join(DPATH_ANONYMOUS, args.file)
    output_path = os.path.join(DPATH_ANONYMOUS, args.out)

    #read anonymous tabel 
    df = pd.read_excel(input_path)

    print("file size:", df.shape)
    print(df.head)

    #if dictionary does not exist yet (first execute) - create one
    dict_path = os.path.join(DPATH_ANONYMOUS, DICT_FILE) 
    if not os.path.exists(dict_path):
        createDictionary(df, dict_path)

    #translate 
    translate(df, dict_path)

    #save translated file 
    with pd.ExcelWriter(output_path, datetime_format='DD/MM/YYYY') as writer:
        df.to_excel(writer, index =False)




    






   

