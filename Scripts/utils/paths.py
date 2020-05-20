
import sys
import os
import json
import argparse
import pandas as pd
import numpy as np
import datetime
import sklearn

# solution to my problem I had: didn't recognize conda
# https://github.com/numpy/numpy/issues/15183

#definitions 

ROOT_PATH = os.path.dirname(os.path.dirname(sys.path[0])) #"C:/Users/hp4mp/PythonProjects/Anastomotic-Leak-Prediction/"

DATA_PATH = os.path.join(ROOT_PATH, "Data") 

DPATH_MATRICES =  os.path.join(DATA_PATH, "matrices")  

DPATH_SOURCES = os.path.join(DATA_PATH, "sourceFiles")  

DPATH_EVENTS = DATA_PATH + "organizeEvents/"

DICT_PATH = ROOT_PATH + "MetaData/Hebrew_English_Dictionary/"

