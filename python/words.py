import plos, string, csv
from Stemmer import Stemmer
from math import log

__stopwords__ = [f.replace('\n','') for f in open('stopwords.txt').readlines()]
__stemmer__ = Stemmer('english')

def clean(word):
    return ''.join(filter(lambda x: x in string.printable and x not in string.punctuation, word.lower())) 


def stem(word):
    return __stemmer__.stemWord(clean(word))

def accept(word):
    word = clean(word) 
    return len(word) > 0 and word not in __stopwords__ 

class counter:
    '''
    Object to build word-count vectors using a corpus.  Must be constructed using a corpus of texts so that a 
    global dictionary can be created; thereafter vectors are created only from the words in the dictionary.

    In addition to the vector methods, this provides access to three properties that may be useful:
    doccounts - a map of words and the number of documents in which they appear
    words - a sorted list of the words
    total_docs - the total number of documents used in the dictionary
    '''

    def __init__(self,texts,mindocs=1,maxdocs=None,dictionaryFile=None):
        '''
        texts - training set of texts from which to build a global dictionary
        mindocs - the minimum number of documents a (stemmed) word must appear in to be included in the dictionary
        maxdocs - the maximum number of documents a (stemmed) word can appear in to be included in the dictionary
        dictionaryFile - name of a file in which to store the dictionary, if any
        '''

        self.doccounts = {}
        self.words = []
        self.total_docs = 0

        if isinstance(texts,str):
            texts = [ texts ]
        elif isinstance(texts[0],list):
            texts = [t[0] for t in texts]
        words = [ f.split() for f in texts ]
        words = [ [stem(f) for f in lst if accept(f)] for lst in words ]
        if not maxdocs: maxdocs = len(texts) 
        self.total_docs = len(texts)
    
        #count the number of times each word appears in documents
        for lst in words:
            for word in set(lst):
                if self.doccounts.has_key(word):
                    self.doccounts[word] = self.doccounts[word] + 1
                else:
                    self.doccounts[word] = 1
        total_words = len(self.doccounts)
        #check for words that appear too frequently or infrequently, and remove them
        self.doccounts = dict((word,count) for word, count in self.doccounts.iteritems() if count >= mindocs and count <= maxdocs)
        #store sorted words so vectors are always in the same order
        self.words = sorted(self.doccounts.keys()) 
        #cache the idf values
        self.__idfcache__ = [ log(float(self.total_docs) / self.doccounts[word]) for word in self.words ] 

        print 'created dictionary of %s stemmed words, excluded %s words' % (len(self.doccounts),total_words - len(self.doccounts))

        if dictionaryFile:
            dictionaryFile = open(dictionaryFile,'w')
            print [f + '\n' for f in self.words]
            dictionaryFile.writelines([f + '\n' for f in self.words])
            dictionaryFile.flush()
            dictionaryFile.close()

    def count_vector(self, text):
        '''
        Create a vector of word counts - for each word in the dictionary, count the occurrences in the given text
        '''
        if(isinstance(text,list)):
            text = text[0]
        words = text.split()
        words = [ clean(f) for f in words if accept(f) ]
        return [ words.count(f) for f in self.words ]
 
    def tf_vector(self, text):
        '''
        Create a vector of term frequency values - for each word in the dictionary, return the frequency with which it
        occurs in the given text (the word count divided by the number of dictionary words in the text)
        '''
        counts = self.count_vector(text)
        total = reduce(lambda x,y : x + y, counts)
        return [ float(i) / total for i in counts ]

    def tfidf_vector(self, text):
        '''
        Create a vector of term frequency-inverse document frequency values - for each word in the dictionary, 
        return the TF-IDF value: http://en.wikipedia.org/wiki/Tfidf 
        '''
        tf_vector = self.tf_vector(text)
        return [ tf*idf for tf, idf in zip(tf_vector,self.__idfcache__) ]

class mapper:
    '''
        Maps String categories to indicator vectors of 0s and 1s
        trainingSubjects - list of subjects to create a mapping for. Each element should be either a string or a list of subjects.
        mindocs - the minimum number of documents in which a subject must occur to be included in the list.
            When mapping subjects to vectors, subjects that aren't in the list will be mapped to all 0's
        subjectFile - name of a file in which to store the distinct subjects, in order, if any
    '''
    def __init__(self,trainingSubjects,mindocs=1,subjectFile=None):
        if isinstance(trainingSubjects[0],list):
            trainingSubjects = [ ', '.join(f[0:2]).title() for f in trainingSubjects ]
        subjCounts = {f : trainingSubjects.count(f) for f in set(trainingSubjects)}
        self.sortedSubjs = sorted([sub for sub in subjCounts.keys() if subjCounts[sub] >= mindocs])
        self.count = len(self.sortedSubjs)
        print 'created mapping of %s subjects, excluded %s subjects' % (self.count,len([f for f in subjCounts.keys() if subjCounts[f] < mindocs]))
        if subjectFile:
            subjectFile = open(subjectFile,'w')
            subjectFile.writelines([f + '\n' for f in self.sortedSubjs])
            subjectFile.flush()
            subjectFile.close()

    def vector(self,subject):
        if isinstance(subject,list):
            subject = ', '.join(subject[0:2]).title()
        vector = [0 for i in range(0,self.count)]
        try:
            index = self.sortedSubjs.index(subject) 
            vector[index] = 1
        except ValueError:
            pass
        return vector

    def category(self,vector):
        try:
            return self.sortedSubjs[vector.index(1)]
        except ValueError:
            return 'UNKNOWN'
