import plos, words
from urllib2 import quote
import csv

__incSize__ = 500
__subject__ = 'subject_level_1'
__text__ = 'abstract'

def sample(limit,trainingSetSize):
    fields = 'id,%s,%s' % (__text__, __subject__)
    sort = quote('publication_date desc') 
    documents = []
    for f in range(0,limit,__incSize__):
        documents += plos.search({'fl' : fields, 'sort' : sort, 'rows' : __incSize__, 'start' : f})  

    documents = filter(lambda f: f.has_key(__subject__) and f.has_key(__text__), documents)
    return { 'train' : documents[0:trainingSetSize],
        'test' : documents[trainingSetSize:len(documents)]}
