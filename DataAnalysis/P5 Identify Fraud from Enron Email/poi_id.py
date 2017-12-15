#!/usr/bin/python
#  -*- coding: utf-8 -*-

import sys
import pickle
import numpy as np
import pandas as pd
from pprint import pprint

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
# features_list = ['poi','salary', 'bonus'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Construct DataFrame from ict
raw_df = pd.DataFrame.from_dict(data_dict, orient='index', dtype=np.float)

### reorder the features
payments_features = ['salary', 'bonus', 'long_term_incentive', 'deferred_income', 'deferral_payments',
                     'loan_advances', 'other', 'expenses', 'director_fees', 'total_payments']
stock_features = ['exercised_stock_options', 'restricted_stock', 'restricted_stock_deferred', 'total_stock_value']
email_features = list(set(raw_df.columns) - set(payments_features) - set(stock_features) - {'poi'})
email_features.sort()

raw_df = raw_df[['poi'] + payments_features + stock_features + email_features]

### change poi datatype
raw_df['poi'] = raw_df['poi'].astype(np.bool)

# print(raw_df.info())
# raw_df.head()

### Task 2: Remove outliers
# 删除异常值
df = raw_df.drop(['TOTAL'], errors='ignore')

# 修正 BELFER ROBERT 和 BHATNAGAR SANJAY 的数据
df.loc['BELFER ROBERT'] = df.loc['BELFER ROBERT'][payments_features + stock_features].shift(-1) \
    .append(df.loc['BELFER ROBERT'][email_features + ['poi']])

df.loc['BHATNAGAR SANJAY'] = df.loc['BHATNAGAR SANJAY'][payments_features + stock_features].shift(1) \
    .append(df.loc['BHATNAGAR SANJAY'][email_features + ['poi']])

# 去掉 email_address列
df = df.drop(['email_address'], axis=1, errors='ignore')

# 将所有payment、stock数据的 NaN 值替换为 0
df[payments_features] = df[payments_features].replace(np.nan, 0)
df[stock_features] = df[stock_features].replace(np.nan, 0)


### Task 3: Create new feature(s)

### 定义比例，分子分母加1 防止除以0。
def create_ratio_feature(df, a, b):
    return (df[a] + 1) / (df[b] + 1)

df1 = df.copy()
df1['from_poi_ratio'] = create_ratio_feature(df1, 'from_this_person_to_poi', 'from_messages')
df1['to_poi_ratio'] = create_ratio_feature(df1, 'from_poi_to_this_person', 'to_messages')
df1['shared_poi_ratio'] = create_ratio_feature(df1, 'shared_receipt_with_poi', 'to_messages')
df1['bonus_to_salary'] = create_ratio_feature(df1, 'bonus', 'salary')
df1['payments_to_stock'] = create_ratio_feature(df1, 'total_payments', 'total_stock_value')

df1 = df1.replace(np.nan, 0)


### Store to my_dataset for easy export below.
my_dataset = df1.to_dict(orient='index')
features_list = df1.columns

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.cross_validation import train_test_split

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

clf = GaussianNB()
clf.fit(features_train, labels_train)
predictions = clf.predict(features_test)
print("GaussianNB \t precision: %.3f, recall: %.3f, f1-score: %.3f" % (
    precision_score(labels_test, predictions),
    recall_score(labels_test, predictions),
    f1_score(labels_test, predictions)
))

clf = SVC()
clf.fit(features_train, labels_train)
predictions = clf.predict(features_test)
print("SVC \t precision: %.3f, recall: %.3f, f1-score: %.3f" % (
    precision_score(labels_test, predictions),
    recall_score(labels_test, predictions),
    f1_score(labels_test, predictions)
))

clf = DecisionTreeClassifier()
clf.fit(features_train, labels_train)
predictions = clf.predict(features_test)
print("DecisionTreeClassifier \t precision: %.3f, recall: %.3f, f1-score: %.3f" % (
    precision_score(labels_test, predictions),
    recall_score(labels_test, predictions),
    f1_score(labels_test, predictions)
))


clf = AdaBoostClassifier()
clf.fit(features_train, labels_train)
predictions = clf.predict(features_test)
print("AdaBoostClassifier \t precision: %.3f, recall: %.3f, f1-score: %.3f" % (
    precision_score(labels_test, predictions),
    recall_score(labels_test, predictions),
    f1_score(labels_test, predictions)
))


### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.model_selection import GridSearchCV

clf = AdaBoostClassifier()
parameters = {
    'n_estimators': range(50, 100, 10),
}

grid = GridSearchCV(clf, parameters, scoring='f1', cv=10)
grid.fit(features_train, labels_train)

clf = grid.best_estimator_
predictions = clf.predict(features_test)
print("AdaBoostClassifier \t precision: %.3f, recall: %.3f, f1-score: %.3f" % (
    precision_score(labels_test, predictions),
    recall_score(labels_test, predictions),
    f1_score(labels_test, predictions)
))

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)