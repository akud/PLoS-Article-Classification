import plos, words
from urllib2 import quote
import csv

__incSize__ = 500

def sample(limit,trainingSetSize,*args):
    fields = 'id,%s' % (','.join(args))
    sort = quote('publication_date asc') 
    documents = []
    for f in range(0,limit,__incSize__):
        documents += plos.search(
            {'fl' : fields, 'sort' : sort,
            'rows' : __incSize__, 'start' : f})  

    documents = filter(lambda doc: False not in [doc.has_key(field) for field in args], documents)
    return { 'train' : documents[0:trainingSetSize],
        'test' : documents[trainingSetSize:len(documents)]}
