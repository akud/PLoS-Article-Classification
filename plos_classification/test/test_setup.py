from unittest import TestCase, main
import plos_classification.setup as setup

class TestLimit(TestCase):

    def runTest(self):
        sample = setup.sample(100,85,'id','abstract','title')
        self.assertEqual(len(sample),2)
        self.assertTrue(len(sample['train']) <= 85)
        self.assertTrue(len(sample['test']) <= 15)

        for f in sample['train']:
            for arg in ['id','abstract','title']:
                self.assertIn(arg,f.keys())

        for f in sample['test']:
            for arg in ['id','abstract','title']:
                self.assertIn(arg,f.keys())
    

if __name__ == '__main__':
    main()
