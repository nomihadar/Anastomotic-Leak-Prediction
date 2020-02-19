
import sys
import pandas as pd
import numpy as np
import datetime
from IPython.display import display

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 200)
#pd.set_option('display.float_format', lambda x: '%.f' % x)
pd.options.display.precision = 4

#import sys
np.set_printoptions(threshold=sys.maxsize) #- print the full NumPy array

from myDefs.defs import *

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def fun(df, events):

    g = events.groupby('feature_name')

    s = g['feature_name']
    #print(g.groups.keys())

    #print(g['feature_name'].count())

    features_names = events[events['feature_name'].notna()][['eventName', 'feature_name']]
    print(features_map)

    features_map = features_names.to_dict()

    print(features_map)

    pass



if __name__ == '__main__':
    # Read events file
    path = DATA_PATH + "parseData1.csv"
    df = pd.read_csv(path, sep=',')

    # Read Events file
    path = "{}organizeEvents/all_events_manual.xlsx".format(DATA_PATH)
    events = pd.read_excel(path)

    fun(df, events)

    # Read Anonymous file
    path = "{}parseAnonymous0.csv".format(DATA_PATH)
    anonymous = pd.read_csv(path, sep=',')



    display(events.head())


