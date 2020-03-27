import sys
import pandas as pd
import numpy as np
import datetime
import json

#definitions 

ROOT_PATH = "C:/Users/hp4mp/PythonProjects/Anastomotic-Leak-Prediction/"

DATA_PATH = ROOT_PATH + "Data/"

SOURCE_DATA_PATH = DATA_PATH + "sourceFiles/"

ORGANIZE_EVENTS_PATH = DATA_PATH + "organizeEvents/"

DICT_PATH = ROOT_PATH + "MetaData/Hebrew_English_Dictionary/"

WRITE_FLAG = False


#if string contains Hebrew chars
def containHebrewChars(s):
    return any("\u0590" <= c <= "\u05EA" for c in s)


#returns list of Hebrew words in a given df 
def getHebrewWords(df):
    
    hebrewVals = []

    #for each column
    for column in df:
        
        #if type of column is string 
        if df[column].dtype == object:
            #get unique values
            uniqueVals = df[column].astype(str).unique()
            #get Hebrew values
            hebrew = [val for val in uniqueVals if containHebrewChars(val)]
            #save words
            hebrewVals.extend(hebrew)

    return pd.DataFrame({"words": hebrewVals})

