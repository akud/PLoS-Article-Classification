from unittest import main, TestCase
import plos_classification.load_data as load_data

class TestLoadData(TestCase):
    def setUp(self):
        self.xFile = 'data/test/test_x.csv'
        self.yFile = 'data/test/test_y.csv'
        self.expectedX = [
            [1,0,4,5.5],
            [1.2,7.9,10,11]
        ]
        self.expectedY = [
            0,
            1,
            -1
        ]
    def runTest(self):
        x,y = load_data.load(self.xFile,self.yFile) 
        self.assertEqual(x,self.expectedX)
        self.assertEqual(y,self.expectedY)
    
if __name__ == '__main__':
    main()
