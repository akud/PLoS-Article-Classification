import plos, words
from urllib2 import quote
import csv

__incSize__ = 500
subjectField = 'subject_level_1'
textField = 'abstract'

def sample(limit,trainingSetSize):
    fields = 'id,%s,%s' % (textField, subjectField)
    sort = quote('publication_date desc') 
    documents = []
    for f in range(0,limit,__incSize__):
        documents += plos.search(
            {'fl' : fields, 'sort' : sort,
            'rows' : __incSize__, 'start' : f})  

    documents = filter(lambda f: f.has_key(subjectField) and len(f[subjectField][0]) > 0
        and f.has_key(textField) and len(f[textField][0]) > 0, documents)
    return { 'train' : documents[0:trainingSetSize],
        'test' : documents[trainingSetSize:len(documents)]}
