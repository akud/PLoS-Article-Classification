#!/usr/bin/python

import setup, csv, words
from datetime import datetime

s = setup.sample(10000,6000)

print datetime.now(), 'finished gathering sample articles'

csv.writer(open('test_ids.csv','w')).writerow([f['id'] for f in s['test']])
csv.writer(open('train_ids.csv','w')).writerow([f['id'] for f in s['train']])

counter = words.counter([f[words.__text__][0] for f in s['train'] if len(f[words.__text__][0]) > 0)
mapper = words.mapper([f[words.__subject__][0] for f in s['train'] if len(f[words.__subject__][0]) > 0)

train = csv.writer(open('train.csv','w'))
test = csv.writer(open('test.csv','w')) 
ytrain = csv.writer(open('ytrain.csv','w')) 
ytest = csv.writer(open('ytest.csv','w')) 

print datetime.now(), 'converting to vectors and storing to csv'
for f in [f[words.__text__][0] for f in s['train'] if len(f[words.__text__][0]) > 0]:
    train.writerow(f)
for f in [f[words.__subject__][0] for f in s['train'] if len(f[words.__text__][0]) > 0]:
    ytrain.writerow(f)

for f in [f[words.__text__][0] for f in s['test'] if len(f[words.__text__][0]) > 0]:
    test.writerow(f)
for f in [f[words.__subject__][0] for f in s['test'] if len(f[words.__text__][0]) > 0]:
    ytest.writerow(f)

print datetime.now(), 'finished'
