from myDefs.defs import *
from IPython.display import display

pd.set_option('display.max_columns', 300)
pd.set_option('display.max_rows', 100)
#pd.set_option('display.float_format', lambda x: '%.f' % x)
pd.options.display.precision = 4

#import sys
np.set_printoptions(threshold=sys.maxsize) #print the full NumPy array

WRITE_FLAG = True

INPUT_PATH0 = DATA_PATH + "parseData2.csv"
INPUT_PATH1 = DATA_PATH + "parseAnonymous0.csv"
OUTPUT_PATH = DATA_PATH + 'matrix1.xlsx'


def readData(path):
    # read events data
    df = pd.read_csv(path, sep=',')
    # parse date of surgery
    df['eventStartDate'] = pd.to_datetime(df['eventStartDate'], format='%Y-%m-%d')
    df['eventEndDate'] = pd.to_datetime(df['eventEndDate'], format='%Y-%m-%d')
    return df

def readAnonymous(path):
    # read annonymous file
    anonymous = pd.read_csv(path, sep=',')
    # parse date of surgery
    anonymous['Date of surgery'] = pd.to_datetime(anonymous['Date of surgery'], format='%Y-%m-%d')

    return anonymous

def organizeAnonymous(anonymous):

    # get only patient with a surgery date, which are not duplicate (first surgey)
    anonymous = anonymous[anonymous['Date of surgery'].notna()].loc[~anonymous['pid'].duplicated()]
    print("anonymous:", anonymous.shape)

    # get data from anonymous

    # map 1 if Anastomotic Leak, 0 o.w.
    anonymous['Anastomotic Leak'] = 0
    anonymous.loc[anonymous['Complications'] == 'Anastomotic Leak', 'Anastomotic Leak'] = 1

    # drop columns
    cols_to_remove = ['Name of surgery',
                      'Days of hospitalization', 'Patient classification',
                      'Responsible surgeon', 'Kk', 'Simple', 'Severe', 'Complications']
    anonymous = anonymous.drop(columns=cols_to_remove).set_index('pid')

    #print ("Anonymous:")
    #display(anonymous)

    return anonymous


def selectEvents(df, category, npatients=1):
    slice = df[df['inModel'] == 1].loc[df['category'] == category].loc[
        df.groupby('featureName')['pid'].transform('nunique') > npatients].index
    print(category, "length:", len(slice))

    return slice

if __name__ == '__main__':

    # Read files
    df = readData(INPUT_PATH0)
    anonymous = readAnonymous(INPUT_PATH1)

    print("data size:", df.shape)
    print("anonymous size:", anonymous.shape)

    # Filter events and slice data
    anonymous = organizeAnonymous(anonymous)

    # filter patients not in anonymous
    df = df[df['pid'].isin(anonymous.index)]
    nuniquePatients = df['pid'].nunique()
    print ("num unique patients:", nuniquePatients)

    #select events
    laboratory = selectEvents(df, "laboratory")
    physical = selectEvents(df, "physical")
    drug = selectEvents(df, "drug")

    # slice events
    data = df.loc[laboratory | physical | drug]

    print("data shape after selecting events:", data.shape)

    #print chosen features
    #print("chosen events:")
    #print(data['featureName'].value_counts().sort_values(ascending=False))

    # # Create A Features Table

    # ### MAT0: Anonymous

    mat0 = pd.concat([anonymous], axis=1, keys=["general"], names = [""])
    mat0 = pd.concat([mat0], axis=1, keys=["constant"], names = [""])
    mat0.columns = mat0.columns.reorder_levels([1,2,0])
    mat0

    # ### MAT1: laboratory & physical categories
    data = df.loc[laboratory | physical]

    before_frames = []
    after_frames = []

    #for each patient and surgery date in anonymous
    for pid, row in anonymous.iterrows():

        #get surgery date of current patient
        surgery_date = row['Date of surgery']

        #print(pid, surgery_date)

        #get events before and after date of surgery
        patient = data.loc[data['pid'] == pid, :]
        before = patient[patient['eventStartDate'] < surgery_date]
        after = patient[patient['eventStartDate'] >= surgery_date]

        #print(row['pid'], "nBefore:", len(before), "nAfter:", len(after))

        #calculate statistics
        x1 = before.groupby('featureName')['numeric'].agg(['mean', 'median', 'min', 'max'])
        x2 = after.groupby('featureName')['numeric'].agg(['mean', 'median', 'min', 'max'])

        #reshape and add pid
        y1 = x1.stack().to_frame().T.assign(pid=pid)
        y2 = x2.stack().to_frame().T.assign(pid=pid)

        #add to list
        before_frames.append(y1)
        after_frames.append(y2)

        #display(y1)
        #display(y2)

    #y1 = pd.concat([x1], keys=['before_surgery'], names=['date'])
    #y2 = pd.concat([x2], keys=['after_surgery'], names=['date'])

    before_concat = pd.concat(before_frames).set_index('pid', drop=True)
    after_concat = pd.concat(after_frames).set_index('pid', drop=True)

    mat1 = pd.concat([before_concat, after_concat], axis=1,
                            keys=['before_surgery', 'after_surgery'],
                            names=['time','eventName', 'statistic'])

    print("before shape:", before_concat.shape, "Num events:", before_concat.columns.get_level_values(0).nunique())
    print("after shape:", after_concat.shape, "Num events:", after_concat.columns.get_level_values(0).nunique())
    print("result shape:", mat1.shape)

    #display(mat1.head())

    #print(mat1.columns.nlevels)
    #print(mat1.columns)

    # ### MAT2: drug category

    data = df.loc[drug]

    mat2 = data.loc[:,['pid', 'featureName']].groupby(['pid', 'featureName']).apply(len).unstack().fillna(0)

    mat2 = pd.concat([mat2], axis=1, keys=['all_days'], names = ["time"])
    mat2 = pd.concat([mat2], axis=1, keys=['count'], names = ["statistic"])
    mat2.columns = mat2.columns.reorder_levels([1,2,0])

    mat2

    # ### MATRIX: combine matrices

    matrix = pd.concat([mat0, mat1, mat2], axis=1, keys=['metadata', 'numeric_events', 'drugs'])
    matrix = matrix.drop(columns=['Date of surgery'], level=2)
    matrix.columns = matrix.columns.set_names(['type', 'time','feature', 'statistic'])
    #display(matrix.head())

    #

    # # Write outputs

    #write output
    if WRITE_FLAG:
        matrix.to_excel(OUTPUT_PATH)


