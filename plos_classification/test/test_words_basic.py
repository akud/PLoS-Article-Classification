import plos_classification.words as words
from unittest import TestCase, main

class TestClean(TestCase):
    def setUp(self):
        self.words = {
            u'hello.' : 'hello',
            u'HELlo-WOrld' : 'helloworld',
            u'\u201cbest\u201d ' : 'best',
            u'TH\nis\tis\rthe' : 'thisisthe'           
        }

    def runTest(self):
       for word in self.words.keys():
           self.assertEqual(words.clean(word),self.words[word])

class TestStem(TestCase):
    def setUp(self):
        self.words = {
            u'relaxing' : 'relax',
            u' insouciance\u201c' : 'insouci',
            u'\t\rrelaxation\n' : 'relax'
        }

    def runTest(self):
        for word in self.words.keys():
            self.assertEqual(words.stem(word),self.words[word])
   
class TestAccept(TestCase):
    def setUp(self):
        self.words = {
            u'relaxing' : True,
            u' \u201c' : False,
            u'a' : False,
            u'they\'re' : False
        }

    def runTest(self):
        for word in self.words.keys():
            self.assertEqual(words.accept(word),self.words[word])
 
if __name__ == '__main__':
    main()
