#!/usr/bin/python
''' 
Script to gather sample articles from solr and write them to json
'''
import plos_classification.setup as setup, json
from datetime import datetime

print datetime.now(), 'gathering sample articles'
s = setup.sample(15000,10000,'abstract','title','subject2_hierarchy','cross_published_journal_key')

print datetime.now(), 'writing sample to file'
o = open('data/sample.json','w')
json.dump(s,o,indent=2)

print datetime.now(),'finished'
