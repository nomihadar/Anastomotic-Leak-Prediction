
from myDefs.defs import *

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report
from sklearn import metrics
from IPython.display import display

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 200)
#pd.set_option('display.float_format', lambda x: '%.f' % x)
pd.options.display.precision = 4

#import sys
np.set_printoptions(threshold=sys.maxsize) #- print the full NumPy array

WRITE_FLAG = False
INPUT_PATH = DATA_PATH + 'pre_matrix0.xlsx'
OUTPUT_PATH0 = DATA_PATH + 'matrix0_missing_values.xlsx'
OUTPUT_PATH1 = DATA_PATH + 'matrix0.xlsx'

def plot_pie(y):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'No AL', 'Anastomotic Leak (AL)'
    sizes = [len(y) - y.sum(), y.sum()]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def plot_my_confusion_matrix(classifier, X_test, y_test):

    # Plot non-normalized confusion matrix
    titles_options = [("Confusion matrix, without normalization", None),
                      ("Normalized confusion matrix", 'true')]
    for title, normalize in titles_options:
        disp = plot_confusion_matrix(classifier, X_test, y_test,
                                     display_labels=["Leak", "no Leak"],
                                     cmap=plt.cm.Blues,
                                     normalize=normalize)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()

df = pd.read_excel(INPUT_PATH, header=[0,1,2,3], index_col=0)
print("Loaded matrix shape:", df.shape)

############################
# process data
############################

n = df.columns.get_level_values('feature').nunique() - df['metadata'].shape[1]
print("Num features before dropping columns:", n)

#filter columns by number of patients
npatients = df.shape[0]

#filter "numeric events" columns
v = df[['numeric_events']].notna().sum().lt(npatients*0.50)
df.drop(v.index[v], axis=1, inplace=True)

#filter drugs columns
v = df[['drugs']].notna().sum().lt(npatients*0.20)
df.drop(v.index[v], axis=1, inplace=True)

n = df.columns.get_level_values('feature').nunique() - df['metadata'].shape[1]
print("Num features after dropping columns:", n)

if WRITE_FLAG:
    df.to_excel(OUTPUT_PATH0)

    #features = df.columns.get_level_values('feature').drop_duplicates().to_frame()
    #features.to_excel(DATA_PATH + 'matrix0_fatures.xlsx', index=False)

features = df.columns.get_level_values('feature').drop_duplicates()


#fill numeric events with median
df['numeric_events'] = df['numeric_events'].fillna(df['numeric_events'].median())

#fill missing values in dtugs with 0
df['drugs'] = df['drugs'].fillna(0)

#fill age with median
df.iloc[:,1] = df.iloc[:,1].fillna(df.iloc[:,1].median())

if WRITE_FLAG:
    df.to_excel(OUTPUT_PATH1)

############################
# model- Logistic Regression
############################

#Get x and y
to_drop = [df.columns[0], df.columns[2], df.columns[3], df.columns[4]]
x = df.drop(columns=to_drop)
y = df.iloc[:, 4]


# Exploration

# print percentage of 0,1
print("\nNum of anastomotic leak (AL):")
p = y.value_counts()
p.index = ["AL", "no-AL"]
p.name = ""
display(p)
percent = y.sum()/len(y)
print("\nPercentage of AL: {:.2f}%".format(percent*100))
plot_pie(y)

#train - test

#The stratify parameter makes a split so that the proportion of values in the sample produced
#will be the same as the proportion of values provided to parameter stratify.

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.2,
                                                    random_state=0,
                                                    stratify=y)

traintest = pd.concat([y_train.value_counts(), y_test.value_counts()], axis=1)
traintest.columns = ['y_train', 'y_test']
traintest['total'] = traintest['y_train'] + traintest['y_test']
traintest

#Create a Model and Train It
model = LogisticRegression(solver='lbfgs', max_iter=100000)
model.fit(x_train, y_train)

############################
# Performances
############################

# Performances
y_pred = model.predict(x_test)
score = model.score(x_test, y_test)
print('\nAccuracy of logistic regression classifier on test set: {:.2f}'.format(score))

#precision is the ratio tp / (tp + fp)
"accuracy: {:.2f}".format((88+4)/(105))

#plot confusion matrix
confusion_matrix = confusion_matrix(y_test, y_pred)

plot_my_confusion_matrix(model, x_test, y_test)
print(classification_report(y_test, y_pred))

logit_roc_auc = metrics.roc_auc_score(y_test, y_pred)
fpr, tpr, thresholds = metrics.roc_curve(y_test, model.predict_proba(x_test)[:,1])

plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = {:.2f})'.format(logit_roc_auc))
plt.plot([0, 1], [0, 1],'r--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve')
plt.legend(loc="lower right")
plt.show()

y_train


