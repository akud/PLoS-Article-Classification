import plos, string, re, csv
from Stemmer import Stemmer

class counter:
    '''
        Object to build word count vectors from texts.  Instances are created with 
        a whole set of training documents from which to build a global dictionary.
    '''

    def __init__(self,texts,normalize=True,appendWordCount=False,dictionaryFile=None):
        '''
        texts - training set of texts from which to build a global dictionary
        normalize - whether vectors produced by this object should have their entries divided by the total number of words
        appendWordCount - whether to append the word count to the end of vectors (after normalization, if any)
        storeDictionary - whether to write the dictionary out to a file
        '''

        self.__stopwords__ = [f.replace('\n','') for f in open('stopwords.txt').readlines()]
        self.__stemmer__ = Stemmer('english')
        self.normalize = normalize
        self.appendWordCount = appendWordCount
        self.punc = re.compile('[^a-zA-Z]')
#build the global dictionary
        if isinstance(texts,str):
            texts = [ texts ]
        words = reduce(lambda x,y: x + y, [ f.split() for f in texts ])
        words = [ self.removePunctuation(f.lower()) for f in words if f not in self.__stopwords__]
        words = [self.__stemmer__.stemWord(f) for f in words]
        
        self.dic = sorted(list(set(words)))
        self.dic.remove('')
        print 'created dictionary of %s stemmed words' % (len(self.dic))
        if dictionaryFile:
            csv.writer(open(dictionaryFile,'w')).writerow(self.dic)

    def vector(self,text):
        '''
        Build a vector of word counts from the global dictionary in the given text
        '''
        words = text.lower().split()
        words = [self.__stemmer__.stemWord(self.removePunctuation(f)) for f in words if f not in self.__stopwords__]
        counts = [ words.count(f) for f in self.dic]
        if self.normalize: counts = [ float(i) / len(words) for i in counts ]
        if self.appendWordCount: counts += [len(words)]
        return counts

    def removePunctuation(self,word):
        return self.punc.sub('',word) 

class mapper:
    '''
        Maps String categories to indicator vectors of 0s and 1s
    '''
    def __init__(self,trainingSubjects,subjectFile=None):
        distinct = set(trainingSubjects)
        self.count = len(distinct)
        self.sortedSubjs = sorted(list(distinct))
        print 'created mapping of %s distinct subjects' % (self.count)
        if categroyFile:
            csv.writer(open(subjectFile,'w')).writerow(self.sortedSubjs)

    def vector(self,subject):
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
