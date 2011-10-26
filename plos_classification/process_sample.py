#!/usr/bin/python
import csv, words, json
from datetime import datetime

s = json.load(open('../data/sample.json')) 
subject_field = 'cross_published_journal_key'
filter_journals = ['PLoSClinicalTrials','PLoSCollections']
text_fields = ['title','abstract']

#write the ids just in case we want them
train_ids = open('../data/train_ids.txt','w')
train_ids.writelines([f['id'] + '\n' for f in s['train']])
train_ids.flush()
train_ids.close()

test_ids = open('../data/test_ids.txt','w')
test_ids.writelines([f['id'] + '\n' for f in s['test']])
test_ids.flush()
test_ids.close()

#csv writers 
train = csv.writer(open('../data/train.csv','w'))
test = csv.writer(open('../data/test.csv','w')) 
ytrain = csv.writer(open('../data/ytrain.csv','w')) 
ytest = csv.writer(open('../data/ytest.csv','w')) 

#set up the word counters
mindocs = round(0.01*len(s['train']))
maxdocs = round(0.99*len(s['train']))

print datetime.now(), 'creating subject mapping'
mapper = words.mapper([filter( lambda x: x not in filter_journals, f[subject_field]) for f in s['train']],
    subjectFile='../data/subjects.txt')

wordcounters = {} 
for textfield in text_fields:
    print datetime.now(), 'creating dictionary for %s' % (textfield)
    wordcounters[textfield] = words.counter([f[textfield] for f in s['train']],
        mindocs=mindocs,maxdocs=maxdocs,dictionaryFile='../data/dictionary-%s.txt' %(textfield))

#process the sample and write vectors
print datetime.now(), 'converting texts to vectors and storing to csv'
for f in s['train']:
    train.writerow(reduce(lambda x,y: x+y,
        [ wordcounters[textfield].tfidf_vector(f[textfield]) for textfield in text_fields]))
    ytrain.writerow(mapper.vector(filter(lambda x : x not in filter_journals, f[subject_field])))

for f in s['test']:
    test.writerow(reduce(lambda x,y: x+y,
        [ wordcounters[textfield].tfidf_vector(f[textfield]) for textfield in text_fields]))
    ytest.writerow(mapper.vector(filter(lambda x : x not in filter_journals, f[subject_field])))

print datetime.now(), 'finished'
