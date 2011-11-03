from unittest import main, TestCase
import plos_classification.load_data as load_data
import numpy, json

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
    def test_standard_load(self):
        x,y = load_data.load(self.xFile,self.yFile) 
        self.assertEqual(x,self.expectedX)
        self.assertEqual(y,self.expectedY)

    def test_numpy_load(self):
        x,y = load_data.load(self.xFile,self.yFile,np=True) 
        array_type = type(numpy.array([]))
        self.assertIsInstance(x,array_type)
        self.assertIsInstance(y,array_type)

        self.assertEqual(len(x),len(self.expectedX))
        for i in range(0,len(x)):
            self.assertEqual(len(x[i]),len(self.expectedX[i]))
            for j in range(0,len(x[i])):
                self.assertEqual(x[i,j],self.expectedX[i][j])

        self.assertEqual(len(y),len(self.expectedY))
        for i in range(0,len(y)):
            self.assertEqual(y[i],self.expectedY[i])


if __name__ == '__main__':
    main()
