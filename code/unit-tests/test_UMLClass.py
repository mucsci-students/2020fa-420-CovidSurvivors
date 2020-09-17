import unittest

import sys
sys.path.append('../')

from UMLClass import UMLClass

class TestUMLClass(unittest.TestCase):
        
    # create a new class called class1
    class1 = UMLClass('class1')

    def test_add_attribute(self, class1):
        
        # test to see if the name of the class is what we declared it
        self.assertEqual(class1.name, 'class1')

        # we haven't added any attributes to our class
        # check to see if list of attributes is empty
        self.assertEqual(class1.attributes, [])

        # add an attribute to class1
        class1.add_attribute('A')
        # test to see if the attribute is in the list of attributes
        self.assertEqual(class1.attributes, ['A'])

        # add two additional attributes to the list
        class1.add_attribute('B')
        class1.add_attribute('C')
        # test to see if the attributes that we added are in our list of attributes
        self.assertEqual(class1.attributes, ['A', 'B', 'C'])
    
    # def test_remove_attribute(self, class1):
        





if __name__ == '__main__':
    unittest.main()