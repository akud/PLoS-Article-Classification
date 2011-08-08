import plos, string, re, csv
from Stemmer import Stemmer

class counter:
    '''
        Object to build word count vectors from texts.  Instances are created with 
        a whole set of training documents from which to build a global dictionary.
    '''

    def __init__(self,texts,mindocs=1,maxdocs=None,normalize=True,appendWordCount=False,dictionaryFile=None):
        '''
        texts - training set of texts from which to build a global dictionary
        mindocs - the minimum number of documents a (stemmed) word must appear in to be included in the dictionary
        maxdocs - the maximum number of documents a (stemmed) word can appear in to be included in the dictionary
        normalize - whether vectors produced by this object should have their entries divided by the total number of words
        appendWordCount - whether to append the word count to the end of vectors (after normalization, if any)
        dictionaryFile - name of a file in which to store the dictionary, if any
        '''

        self.stopwords = [f.replace('\n','') for f in open('stopwords.txt').readlines()]
        self.stemmer = Stemmer('english')
        self.normalize = normalize
        self.appendWordCount = appendWordCount
        self.re = re.compile('[^a-zA-Z]')
#build the global dictionary
        if isinstance(texts,str):
            texts = [ texts ]
        words = [ f.split() for f in texts ]
        words = [ [self.clean(f) for f in lst if f.lower() not in self.stopwords] for lst in words ]
#count the number of times each word appears in documents
        counts = {}
        for lst in words:
            for word in set(lst):
                if counts.has_key(word):
                    counts[word] = counts[word] + 1
                else:
                    counts[word] = 1
        if not maxdocs: maxdocs = len(texts) 
        self.dic = sorted([word for word in counts.keys() if counts[word] >= mindocs and 
            counts[word] <= maxdocs and len(word) > 0])
        print 'created dictionary of %s stemmed words, excluded %s words' % (len(self.dic),len(counts) - len(self.dic))
        if dictionaryFile:
            dictionaryFile = open(dictionaryFile,'w')
            dictionaryFile.writelines([f + '\n' for f in self.dic])
            dictionaryFile.flush()
            dictionaryFile.close()

    def vector(self,text):
        '''
        Build a vector of word counts from the global dictionary in the given text
        '''
        words = text.split()
        words = [self.clean(f) for f in words if f.lower() not in self.stopwords]
        counts = [ words.count(f) for f in self.dic]
        if self.normalize: 
            total = reduce(lambda x,y : x + y, counts)
            try:
                counts = [ float(i) / total for i in counts ]
            except ZeroDivisionError:
                counts = [0 for i in counts ]
        if self.appendWordCount: counts.append(len(words))
        return counts

    def clean(self,word):
        word = self.re.sub('',word.lower()) 
        return self.stemmer.stemWord(word)

class mapper:
    '''
        Maps String categories to indicator vectors of 0s and 1s
        trainingSubjects - list of subjects to create a mapping for
        mindocs - the minimum number of documents in which a subject must occur to be included in the list.
            When mapping subjects to vectors, subjects that aren't in the list will be mapped to all 0's
        subjectFile - name of a file in which to store the distinct subjects, in order, if any
    '''
    def __init__(self,trainingSubjects,mindocs=1,subjectFile=None):
        subjCounts = {f : trainingSubjects.count(f) for f in set(trainingSubjects)}
        self.sortedSubjs = sorted([sub for sub in distinct if subjCounts[sub] >= mindocs])
        self.count = len(self.sortedSubjs)
        print 'created mapping of %s subjects, excluded %s subjects' % (self.count,len([f for f in subjCounts.keys() if subjCounts[f] < mindocs]))
        if subjectFile:
            subjectFile = open(subjectFile,'w')
            subjectFile.writelines([f + '\n' for f in self.sortedSubjs])
            subjectFile.flush()
            subjectFile.close()

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
