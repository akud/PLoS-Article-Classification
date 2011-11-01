import solr
from urllib2 import quote

__defaultInc__ = 500

def sample(limit,trainingSetSize,*args):
    def accept(doc):
        haskeys = False not in [doc.has_key(field) for field in args] 
        if haskeys:
            return 0 not in [len(doc[field][0])
                if isinstance(doc[field],list) else len(doc[field]) for field in args]
        else:
            return False
    fields = 'id,%s' % (','.join(args))
    sort = quote('publication_date asc') 
    documents = []
    increment = __defaultInc__ if limit > __defaultInc__ else limit
    for f in range(0,limit,increment):
        if f + increment > limit: increment = limit - increment
        documents += solr.search(
            {'fl' : fields, 'sort' : sort,
            'rows' : increment, 'start' : f})  

    documents = filter(accept, documents)
    return { 'train' : documents[0:trainingSetSize],
        'test' : documents[trainingSetSize:len(documents)]}
