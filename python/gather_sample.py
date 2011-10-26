#!/usr/bin/python
import setup, json

s = setup.sample(15000,10000,'abstract','title','subject2','cross_published_journal_key')
o = open('../data/sample.json','w')

json.dump(s,o,indent=2)
