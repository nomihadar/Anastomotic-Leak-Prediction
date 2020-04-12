
from myDefs.defs import *

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report
from sklearn import metrics
from IPython.display import display

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 200)
#pd.set_option('display.float_format', lambda x: '%.f' % x)
pd.options.display.precision = 4

#import sys
np.set_printoptions(threshold=sys.maxsize) #- print the full NumPy array

# visualization
import seaborn as sns
import matplotlib.pyplot as plt 
from matplotlib.pyplot import figure

path = DATA_PATH + 'matrix1.xlsx'
df = pd.read_excel(path, header=[0,1,2,3], index_col=0)
print(df.shape)

############################
# process data
############################

#fill numeric events with median
df['numeric_events'] = df['numeric_events'].fillna(df['numeric_events'].median())

#fill missing values in dtugs with 0
df['drugs'] = df['drugs'].fillna(0)

#fill numeric events with median
df.iloc[:,1] = df.iloc[:,1].fillna(df.iloc[:,1].median())

print("After filling missing values:")
display(df.head())

if WRITE_FLAG:
    df.to_excel(DATA_PATH + 'matrix_no_missing.xlsx')

############################
# model- Logistic Regression
############################


#Get x and y
to_drop = [df.columns[0], df.columns[2], df.columns[3], df.columns[4]]
x = df.drop(columns=to_drop)
y = df.iloc[:, 4]

# Exploration
y.value_counts()

sns.countplot(x=y).set(xlabel='Anastomotic Leak', ylabel='count')

percent = y.sum()/len(y)
print("percentage of num Anastomotic leak: {:.2f}%".format(percent*100))

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
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(score))

#precision is the ratio tp / (tp + fp)
"accuracy: {:.2f}".format((88+4)/(105))

#plot confusion matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
confusion_matrix
plot_confusion_matrix(model, x_test, y_test)

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


