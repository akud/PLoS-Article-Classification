#!/usr/bin/python

import setup, csv, words
from datetime import datetime
subjectField = 'subject2_level_1'
textField = 'abstract'

s = setup.sample(15000,10000,subjectField,textField)

print datetime.now(), 'finished gathering sample articles'

train_ids = open('../data/train_ids.txt','w')
train_ids.writelines([f['id'] + '\n' for f in s['train']])
train_ids.flush()
train_ids.close()

test_ids = open('../data/test_ids.txt','w')
test_ids.writelines([f['id'] + '\n' for f in s['test']])
test_ids.flush()
test_ids.close()

mindocs = round(0.01*len(s['train']))
maxdocs = round(0.95*len(s['train']))

counter = words.counter([f[textField] for f in s['train'] if len(f[textField]) > 0],
    normalize=True,mindocs=mindocs,maxdocs=maxdocs,
    dictionaryFile='../data/dictionary.txt')
mapper = words.mapper([f[subjectField][0] for f in s['train'] if len(f[textField]) > 0],
    mindocs=mindocs,subjectFile='../data/subjects.txt')

train = csv.writer(open('../data/train.csv','w'))
test = csv.writer(open('../data/test.csv','w')) 
ytrain = csv.writer(open('../data/ytrain.csv','w')) 
ytest = csv.writer(open('../data/ytest.csv','w')) 

print datetime.now(), 'converting to vectors and storing to csv'
for f in [f[textField] for f in s['train'] if len(f[textField]) > 0 and 1 in mapper.vector(f[subjectField][0])]:
    train.writerow(counter.vector(f))
for f in [f[subjectField][0] for f in s['train'] if len(f[textField]) > 0 and 1 in mapper.vector(f[subjectField][0])]:
    ytrain.writerow(mapper.vector(f))

for f in [f[textField] for f in s['test'] if len(f[textField]) > 0 and 1 in mapper.vector(f[subjectField][0])]:
    test.writerow(counter.vector(f))
for f in [f[subjectField][0] for f in s['test'] if len(f[textField]) > 0 and 1 in mapper.vector(f[subjectField][0])]:
    ytest.writerow(mapper.vector(f))

print datetime.now(), 'finished'
