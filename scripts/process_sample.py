#!/usr/bin/python
import csv, json, plos_classification.words as words
from datetime import datetime

s = json.load(open('data/sample.json')) 
text_fields = ['title','abstract']

#set up csv writers 
train = csv.writer(open('data/xtrain.csv','w'))
test = csv.writer(open('data/xtest.csv','w')) 
ytrain = csv.writer(open('data/ytrain.csv','w')) 
ytest = csv.writer(open('data/ytest.csv','w')) 

mindocs = round(0.01*len(s['train']))
maxdocs = round(0.99*len(s['train']))

#create the subject mapping
print datetime.now(), 'creating subject mapping'
#get the subjects
subjects = [f['subject2_hierarchy'] for f in s['train']]
#take the top-level element of each subject for each doc
subjects = [[sub.split('/')[0] for sub in f] for f in subjects]
#sort and join them together
subjects = [ ''.join(set(sorted(sub))) for sub in subjects]

mapper = words.mapper(subjects, subjectFile='data/subjects.txt')

#setup word counters
wordcounters = {} 
for textfield in text_fields:
    print datetime.now(), 'creating dictionary for %s' % (textfield)

    wordcounters[textfield] = words.counter(
        [f[textfield] for f in s['train']],
        mindocs=mindocs, maxdocs=maxdocs,
        dictionaryFile='data/dictionary-%s.txt' % (textfield))

#process the sample and write vectors
print datetime.now(), 'converting texts to vectors and storing to csv'
for doc in s['train']:
    subject = ''.join(set(sorted([sub.split('/')[0] for sub in doc['subject2_hierarchy']])))
    x = []
    for textfield in text_fields:
        x += wordcounters[textfield].tfidf_vector(doc[textfield])
    train.writerow(x)
    ytrain.writerow(mapper.vector(subject))

for doc in s['test']:
    subject = ''.join(set(sorted([sub.split('/')[0] for sub in doc['subject2_hierarchy']])))
    x = []
    for textfield in text_fields:
        x += wordcounters[textfield].tfidf_vector(doc[textfield])
    train.writerow(x)
    ytrain.writerow(mapper.vector(subject))

print datetime.now(), 'finished'
