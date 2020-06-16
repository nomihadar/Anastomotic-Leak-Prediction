
'''
Edit events sources names by creating list of unique sources and edit manually
'''

import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
from utils.constants import *
 
import pandas as pd

#files names 
INPUT_FILE = "data1.csv"
OUT_FILE = "sourceNamesDict.xlsx"


if __name__ == "__main__":
    
    #read input file  
    input_path = os.path.join(DPATH_DATA, INPUT_FILE) 
    df = pd.read_csv(input_path)
    print("file shape:", df.shape)

    #get sources 
    sources = df['sourceName'].value_counts().sort_values(ascending=False)\
        .rename_axis('sourceName').to_frame('counts')
    
    #write to file 
    output_path = os.path.join(DPATH_DATA, OUT_FILE) 
    if not os.path.exists(output_path):
        sources.to_excel(output_path, index=False)

    #read source names dictionary 
    #sources = pd.read_excel(output_path)
    #sources_dict = dict(zip(sources["sourceName"], sources["alterName"]))
    #df['source'] = df['sourceName'].replace(sources_dict)
  

    
