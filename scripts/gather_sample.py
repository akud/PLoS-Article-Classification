#!/usr/bin/python
import plos_classification.setup as setup, json
from datetime import datetime

print datetime.now(), 'gathering sample articles'
s = setup.sample(15000,10000,'abstract','title','subject2','cross_published_journal_key')

print datetime.now(), 'writing sample to file'
o = open('../data/sample.json','w')
json.dump(s,o,indent=2)

print datetime.now(),'finished'
