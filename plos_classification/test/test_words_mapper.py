from plos_classification.words import mapper
from unittest import TestCase, main

class TestMapper(TestCase):
    def setUp(self):
        categories = [
            'red',
            'yellow',
            'green',
            'blue'
        ]
        self.mapper = mapper(categories)

    def test_sorted(self):
        self.assertEquals(self.mapper.sortedSubjs,
            ['Blue','Green','Red','Yellow']
        )
    def test_vector(self):
        #categories are reordered as ['blue','green','red','yellow']
        self.assertEquals(
            self.mapper.vector('red'),
            [0,0,1,0]
        )
        self.assertEquals(
            self.mapper.vector('yellow'),
            [0,0,0,1]
        )
        self.assertEquals(
            self.mapper.vector('green'),
            [0,1,0,0]
        )
        self.assertEquals(
            self.mapper.vector('blue'),
            [1,0,0,0]
        )

    def test_category(self):
         #categories are reordered as ['blue','green','red','yellow']
        self.assertEquals(
            self.mapper.category([0,0,1,0]),
            'Red',
        )
        self.assertEquals(
            self.mapper.category([0,0,0,1]),
            'Yellow'
        )
        self.assertEquals(
            self.mapper.category([0,1,0,0]),
            'Green'
        )
        self.assertEquals(
            self.mapper.category([1,0,0,0]),
            'Blue'
        )

if __name__ == '__main__':
    main()
