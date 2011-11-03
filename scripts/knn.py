#!/usr/bin/python
'''
Script to run a K - nearest neighbors algorithm and print out the 5-fold cross validation
error for various k
'''
from sklearn import cross_validation, neighbors
from plos_classification.load_data import load
from datetime import datetime

print datetime.now(), 'loading data'
X,y = load('data/xtrain.csv','data/ytrain.csv',np=True)
total = len(X)

print datetime.now(), 'iterating over k'
for k in range(2,11):
    errors = []
    for train_index, test_index in cross_validation.KFold(total,5):
        model = neighbors.KNeighborsClassifier(k)
        model.fit(X[train_index],y[train_index])
        errors.append(model.score(X[test_index],y[test_index]))
    print 'Average error for k = %s: %s' % (k,sum(errors)/len(errors))
