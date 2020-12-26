#!/usr/bin/python
import csv
from sklearn import svm
from datetime import datetime
from sklearn.externals import joblib

print datetime.now(), 'loading csv files'
train_reader = csv.reader(open('data/xtrain.csv'))
ytrain_reader = csv.reader(open('data/ytrain.csv'))
X = []
y = []
for row in train_reader:
    X.append([ float(f) for f in row ])
for row in ytrain_reader:
    y.append(row.index('1'))

print datetime.now(), 'training svm model'
model = svm.SVC()
model.fit(X,y)

print datetime.now(), 'dumping svm model'
joblib.dump(model,'data/svm.pkl')
print datetime.now(), 'finished'
