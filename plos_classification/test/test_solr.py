import plos_classification.solr as solr
import unittest

class TestSingleField(unittest.TestCase):
    def runTest(self):
        res = solr.singlefield('title',5)
        self.assertEqual(len(res),5)
        for title in res:
            self.assertIsInstance(title, unicode)

class TestByIds(unittest.TestCase):
    def setUp(self):
       self.ids = ['10.1371/journal.pcbi.0010001', '10.1371/journal.pcbi.0010002']

    def runTest(self):
        res = solr.byIds(self.ids)
        self.assertEquals(len(res),len(self.ids))
        for doc in res:
            self.assertIn('id',doc.keys())
            self.assertIn('title',doc.keys())
            self.assertIn('abstract',doc.keys())
            self.assertIn(doc['id'],self.ids)

class TestGetIds(unittest.TestCase):
    def runTest(self):
       res = solr.ids(10,5) 
       self.assertIsNotNone(res)
       self.assertEqual(len(res),10)
       for doi in res:
           self.assertIsInstance(doi,unicode)
           self.assertTrue(doi.startswith('10.1371/'))

class TestBasicSearch(unittest.TestCase):
    def runTest(self):
        res = solr.search()
        self.assertEqual(len(res),10)
        for doc in res:
            self.assertIn('id',doc.keys())
            self.assertIn('title',doc.keys())

class TestSearchWithString(unittest.TestCase):
    def runTest(self):
        res = solr.search('*:*')
        self.assertEqual(len(res),10)

        res = solr.search('id:10.1371/journal.pcbi.0010001')
        self.assertEqual(len(res),1)

class TestSearchWithDict(unittest.TestCase):
    def setUp(self):
        self.fields = ['id','title','cross_published_journal_key']


    def runTest(self):
        res = solr.search({
            'q' : '*:*',
            'fl' : ','.join(self.fields),
            'rows' : 2,
            'offset' : 100
            })
        self.assertEqual(len(res),2)
        for doc in res:
            for field in self.fields:
                self.assertIn(field,doc.keys())

if __name__ == '__main__':
    unittest.main()
