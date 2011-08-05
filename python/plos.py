import json
from urllib2 import urlopen, quote
from datetime import datetime, timedelta

searchUrl = 'http://api.plos.org/search?'

def search(query='*:*'):
	'''
		Basic Solr search functionality.

		This takes in a string or dictionary.  If a string is passed, it is assumed to be basic search terms; 
		and if a dictionary is passed, the arguments are passed to solr.

		Returns a list containing dictionary objects for each article found. 
	'''

	if isinstance(query,str): 
		query = { 'q' : query }	
	else:
		if not query.has_key('q'): query['q'] = '*:*' #make sure we include a 'q' parameter
	query['wt'] = 'json' #make sure the return type is json
	query['fq'] = quote('doc_type:full AND !article_type_facet:"Issue Image"') #search only for articles
	query['api_key'] = 'AVbCGmpqdXTRJ9F' 
	
	url = searchUrl;

	for part in query:
		url += '%s%s=%s' % ('&' if url is not searchUrl else '',part,query[part])
	print 'Making request to',url #TEST
	print
	return json.load(urlopen(url),encoding='UTF-8')['response']['docs']

def singleField(field,query={'q': '*:*'}):
    query['fl'] = field
    return [f[field] for f in search(query) if f.has_key(field)]

def byIds(dois,fields='title,abstract'):
    if(isinstance(dois,str)): dois = dois.split(',')
    query = quote(' OR ').join([ 'id:%s' % (f) for f in dois])
    return search({'q' : query, 'fl': fields})

def ids(limit=10,offset=0):
    return singleField('id',
        {'start' : offset, 'rows' : limit,
        'sort' : quote('publication_date desc')})
