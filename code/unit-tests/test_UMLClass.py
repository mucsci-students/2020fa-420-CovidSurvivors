# Unit test for the UMLClass
# Description:     
#   This file validates that each function belonging to the UMLClass class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 17, 2020

##########################################################################
# Imports

import unittest
import sys
sys.path.append('../')
from UMLClass import UMLClass

##########################################################################

# Unit test for the UMLClass
class TestUMLClass(unittest.TestCase):
    
    # validates intended behavior of add_attribute method
    def test_add_attribute(self):
        # create a new class called class1
        class1 = UMLClass('class1')
        # test to see if the name of our class is 'class1'
        self.assertEqual(class1.name, 'class1')

        # we haven't added any attributes to class1
        # check to see if the attributes list for class1 is empty
        self.assertEqual(class1.attributes, [])

        # add an attribute to class1
        class1.add_attribute('A')
        # check to see if the attribute we added are in our class1 attributes list
        self.assertEqual(class1.attributes, ['A'])

        # add two additional attributes to class1
        class1.add_attribute('B')
        class1.add_attribute('C')
        # check to see if the attributes we added are in our class1 attributes list
        self.assertEqual(class1.attributes, ['A', 'B', 'C'])

    ##########################################################################

    # validates intended behavior of remove_attribute method
    def test_remove_attribute(self):
        # create a new class called class2
        class2 = UMLClass('class2')

        # check to see that an exception is raised if the user tries to remove an attribute from
        # the class when no attributes have been added to the attributes list
        with self.assertRaises(ValueError):
            class2.remove_attribute('D')

        # add some attributes to class2
        class2.add_attribute('D')
        class2.add_attribute('E')
        class2.add_attribute('F')
        class2.add_attribute('G')
        # check to see if the attributes we added are in our class2 attributes list
        self.assertEqual(class2.attributes, ['D', 'E', 'F', 'G'])
        
        # remove an existing attribute from class2
        class2.remove_attribute('G')
        # check to see if the attribute we removed has been removed from our class2 attributes list
        self.assertEqual(class2.attributes, ['D', 'E', 'F'])

        # remove another attribute from class2
        class2.remove_attribute('E')
        # check to see if the attribute we removed has been removed from our class2 attributes list
        self.assertEqual(class2.attributes, ['D', 'F'])

        # check to see that an exception is raised if the user tries to remove an attribute that 
        # doesn't exist in our class2 attributes list
        with self.assertRaises(ValueError):
            class2.remove_attribute('Z')

    ##########################################################################

    # validates intended behavior of add_relationship method
    def test_add_relationship(self):
        # create a new class called class3
        class3 = UMLClass('class3')

        # we haven't added any relationips to class3
        # check to see if the relationships list for class3 is empty
        self.assertEqual(class3.relationships, [])

        # add some relationships to our class3 relationships list
        class3.add_relationship('R1')
        class3.add_relationship('R2')
        class3.add_relationship('R3')
        # check to see if the relationships we added are in our class3 relationships list
        self.assertEqual(class3.relationships, ['R1', 'R2', 'R3'])

        # add additional relationships to our class3 relationships list
        class3.add_relationship('R4')
        class3.add_relationship('R5')

        # check to see if the relationships we added are in our class3 relationships list
        self.assertEqual(class3.relationships, ['R1', 'R2', 'R3', 'R4', 'R5'])

    ##########################################################################

    # validates intended behavior of remove_relationship method
    def test_remove_relationship(self):
        # create a new class called class4
        class4 = UMLClass('class4')

        # add some relationships to our class4 relationships list
        class4.add_relationship('R1')
        class4.add_relationship('R2')
        class4.add_relationship('R3')

        # check to see if the relationships we added are in our class4 relationships list
        self.assertEqual(class4.relationships, ['R1', 'R2', 'R3'])

        # remove a relationship from class4
        class4.remove_relationship('R1')
        # check to see if the relationship we removed was removed from our class4 relationships list
        self.assertEqual(class4.relationships, ['R2', 'R3'])

        # remove the rest of the relationships from class4
        class4.remove_relationship('R2')
        class4.remove_relationship('R3')
        # check to see if the relationships we removed were removed from our class4 relationships list
        self.assertEqual(class4.relationships, [])
        
        # check to see that an exception is raised if the user tries to remove a relationsip that 
        # doesn't exist in our class4 relationships list
        with self.assertRaises(ValueError):
            class4.remove_attribute('R1')

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLClass.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLClass.py' command
if __name__ == '__main__':
    unittest.main()