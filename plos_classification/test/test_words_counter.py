from plos_classification.words import counter 
from unittest import TestCase, main

class TestCounter(TestCase):
    def setUp(self):
        self.texts = [
            u'I visited S. F and visited the Conservatory of Flowers and saw the older "Wicked" plants!',
            u'There needs to be a third option because getting older or dying aren\'t working for me.'
        ]
        self.words = [
            u'conservatori', u'die', u'flower', u'get', u'need', u'older', 
            u'option', u'plant', u'saw', u'third', u'visit', u'wick', u'work'
        ]
        self.counts = [
            [1,0,1,0,0,1,0,1,1,0,2,1,0], #counts from the first text
            [0,1,0,1,1,1,1,0,0,1,0,0,1] #counts from the second text
        ] 
        self.idf_values = [ float(0.6931471805599453) for f in self.words ]
        self.idf_values[5] = float(0) #only 'older' is in both texts
 
        self.counter = counter(self.texts)

    def test_words(self):
       self.assertEquals(self.counter.words,self.words)

    def test_idfcache(self):
       self.assertEquals(self.counter.__idfcache__,self.idf_values)

    def test_count_vector(self):
        for i in range(0,2):
            vector = self.counter.count_vector(self.texts[i])
            self.assertEquals(vector,self.counts[i])

    def test_tf_vector(self):
        for i in range(0,2):
            vector = self.counter.tf_vector(self.texts[i])
            total = sum(self.counts[i])
            self.assertEquals(vector,[float(f) / total for f in self.counts[i]])

    def test_tfidf_vector(self):
        for i in range(0,2):
            vector = self.counter.tfidf_vector(self.texts[i])
            total = sum(self.counts[i])
            self.assertEquals(vector,[(float(f) / total)*idf for f,idf in zip(self.counts[i],self.idf_values)])



if __name__ == '__main__':
    main()
