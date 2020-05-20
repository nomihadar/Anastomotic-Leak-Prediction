import os, sys
# solution to my problem I had: didn't recognize conda
# https://github.com/numpy/numpy/issues/15183


'''
Definitions 
'''

ROOT_PATH = os.path.dirname(os.path.dirname(sys.path[0])) #"C:/Users/hp4mp/PythonProjects/Anastomotic-Leak-Prediction/"

#data paths
DATA_PATH = os.path.join(ROOT_PATH, "Data")
DPATH_SOURCES = os.path.join(DATA_PATH, "sourceFiles")  
DPATH_EVENTS = os.path.join(DATA_PATH, "events")  
DPATH_MATRICES =  os.path.join(DATA_PATH, "matrices")  
DPATH_EDA = os.path.join(DATA_PATH, "EDA") #Exploratory Data Analysis 


DICT_PATH = ROOT_PATH + "MetaData/Hebrew_English_Dictionary/"

'''
Constants
'''

#name of Y column 
Y_COL = 'Anastomotic Leak'
#index of Y column
Y_COL_IDX = 0 

#row number(s) to use as the column names
MATRIX_HEADER = [0, 1, 2, 3]


#
WRITE_FLAG = False