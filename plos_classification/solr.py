import json
from urllib2 import urlopen, quote
from datetime import datetime, timedelta
from settings import api_key

searchUrl = 'http://api.plos.org/search?'

def search(query='*:*'):
	'''
		Basic Solr search functionality.

		This takes in a string or dictionary.  If a string is passed, it is assumed to be basic search terms; 
		and if a dictionary is passed, the arguments are passed to solr.

		Returns a list containing dictionary objects for each article found. 
	'''

	if isinstance(query,str): 
		query = { 'q' : quote(query) }	
	else:
		if not query.has_key('q'): query['q'] = '*:*' #make sure we include a 'q' parameter
	query['wt'] = 'json' #make sure the return type is json
	query['fq'] = quote('doc_type:full AND !article_type_facet:"Issue Image"') #search only for articles
	query['api_key'] = api_key
	
	url = searchUrl;

	for part in query:
		url += '%s%s=%s' % ('&' if url is not searchUrl else '',part,query[part])
	print 'Making request to',url #TEST
	print
	return json.load(urlopen(url),encoding='UTF-8')['response']['docs']

def singlefield(field,numrows=10):
    '''
    Query for a single field. Can optionally specify the number of results to return
    '''
    query = {
        'fl' : field,
        'rows' : numrows
    }
    return [f[field] for f in search(query) if f.has_key(field)]

def byIds(dois,fields='title,abstract'):
    '''
    Get the specified fields for the specified dois
    '''
    if(isinstance(dois,str)): dois = dois.split(',')
    if isinstance(fields,list): fields = ','.join(fields)
    if 'id' not in fields: fields = 'id,' + fields

    query = quote(' OR ').join([ 'id:%s' % (f) for f in dois])
    return search({'q' : query, 'fl': fields})

def ids(limit=10,offset=0):
    '''
    Get a list of dois from solr
    '''
    results = search({
        'fl' : 'id',
        'start' : offset,
        'rows' : limit,
        'sort' : quote('publication_date desc')
        })
    return [r['id'] for r in results]
