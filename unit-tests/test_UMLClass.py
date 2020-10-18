# Unit test for the UMLClass
# Description:     
#   This file validates that each function belonging to the UMLClass class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 17, 2020

##########################################################################
# Imports

import unittest
import pytest
import sys
sys.path.append('../')
from models.UMLClass import UMLClass
from models.UMLRelationship import UMLRelationship

##########################################################################

# Unit test for the UMLClass
class TestUMLClass(unittest.TestCase):
    
    # validates intended behavior of add_field method
    def test_add_field(self):
        # create a new class called class1
        class1 = UMLClass('class1')
        # test to see if the name of our class is 'class1'
        self.assertEqual(class1.name, 'class1')

        # we haven't added any fields to class1
        # check to see if the field list for class1 is empty
        self.assertEqual(class1.fields, [])

        # add an field to class1
        class1.add_field('public', 'A', 'string')
        # check to see if the field we added are in our class1 fields list
        self.assertTrue(class1.has_field('A'))

        # add two additional fields to class1
        class1.add_field('private', 'B', 'string')
        class1.add_field('private', 'C', 'string')
        # check to see if the fields we added are in our class1 fields list
        self.assertTrue(class1.has_field('B'))
        self.assertTrue(class1.has_field('C'))

    ##########################################################################

    # validates intended behavior of remove_field method
    def test_remove_field(self):
        # create a new class called class2
        class2 = UMLClass('class2')

        # check to see that an exception is raised if the user tries to remove an field from
        # the class when no fields have been added to the fields list
        with self.assertRaises(IndexError):
            class2.remove_field('D')

        # add some fields to class2
        class2.add_field('public', 'D', 'enum')
        class2.add_field('private', 'E', 'double')
        class2.add_field('private', 'F', 'array')
        class2.add_field('public', 'G', 'int')
        # check to see if the fields we added are in our class2 fields list
        self.assertTrue(class2.has_field('D'))
        self.assertTrue(class2.has_field('E'))
        self.assertTrue(class2.has_field('F'))
        self.assertTrue(class2.has_field('G'))

        # remove an existing field from class2
        class2.remove_field('G')
        # check to see if the field we removed has been removed from our class2 fields list
        self.assertFalse(class2.has_field('G'))

        # remove another field from class2
        class2.remove_field('E')
        # check to see if the field we removed has been removed from our class2 fields list
        self.assertFalse(class2.has_field('E'))

    ##########################################################################

    # validates intended behavior of add_method method
    def test_add_method(self):
        # create a new class called class1
        class1 = UMLClass('class1')
        # test to see if the name of our class is 'class1'
        self.assertEqual(class1.name, 'class1')

        # we haven't added any methods to class1
        # check to see if the method list for class1 is empty
        self.assertEqual(class1.methods, [])

        # add an method to class1
        class1.add_method('public', 'A', 'string')
        # check to see if the method we added are in our class1 methods list
        self.assertTrue(class1.has_method('A'))

        # add two additional methods to class1
        class1.add_method('private', 'B', 'string')
        class1.add_method('private', 'C', 'string')
        # check to see if the methods we added are in our class1 methods list
        self.assertTrue(class1.has_method('B'))
        self.assertTrue(class1.has_method('C'))

    ##########################################################################

    # validates intended behavior of remove_method method
    def test_remove_method(self):
        # create a new class called class2
        class2 = UMLClass('class2')

        # check to see that an exception is raised if the user tries to remove an method from
        # the class when no methods have been added to the methods list
        with self.assertRaises(IndexError):
            class2.remove_method('D')

        # add some methods to class2
        class2.add_method('public', 'D', 'enum')
        class2.add_method('private', 'E', 'double')
        class2.add_method('private', 'F', 'array')
        class2.add_method('public', 'G', 'int')
        # check to see if the methods we added are in our class2 methods list
        self.assertTrue(class2.has_method('D'))
        self.assertTrue(class2.has_method('E'))
        self.assertTrue(class2.has_method('F'))
        self.assertTrue(class2.has_method('G'))

        # remove an existing method from class2
        class2.remove_method('G')
        # check to see if the method we removed has been removed from our class2 methods list
        self.assertFalse(class2.has_method('G'))

        # remove another method from class2
        class2.remove_method('E')
        # check to see if the method we removed has been removed from our class2 methods list
        self.assertFalse(class2.has_method('E'))

    ##########################################################################

    # validates intended behavior of add_relationship method
    def test_add_relationship(self):
        # create a new class called class3
        class3 = UMLClass('class3')
        class4 = UMLClass('class4')
        class5 = UMLClass('class5')

        # we haven't added any relationips to class3
        # check to see if the relationships list for class3 is empty
        self.assertEqual(len(class3.relationships), 0)
        self.assertEqual(len(class4.relationships), 0)
        self.assertEqual(len(class5.relationships), 0)

        # add some relationships to our classes
        class3.add_relationship("inheritance", class5)
        class4.add_relationship("composition", class3)
        class5.add_relationship("aggregation", class4)        
        

        # check to see if the relationships we added are in our class3 relationships list
        self.assertTrue(class3.relationships != [])
        self.assertTrue(class4.relationships != [])
        self.assertTrue(class5.relationships != [])

    ##########################################################################

    # validates intended behavior of remove_relationship method
    def test_remove_relationship(self):
        # create a new class called class4
        class3 = UMLClass('class3')
        class4 = UMLClass('class4')
        class5 = UMLClass('class5')

        # add some relationships to our classes
        class3.add_relationship("inheritance", class5)
        class4.add_relationship("composition", class3)
        class5.add_relationship("aggregation", class4)        

        # remove a relationship from class4
        class4.remove_relationship(class5.name)
        class5.remove_relationship(class4.name)
        # check to see if the relationship we removed was removed from our class4 relationships list
        self.assertTrue(not class4.has_relationship(class5.name))

        # remove the rest of the relationships from class4
        class3.remove_relationship(class4.name)
        # check to see if the relationships we removed were removed from our classes relationships lists
        self.assertEqual(len(class3.relationships), 0)
        
        # check to see that an exception is raised if the user tries to remove a relationsip that 
        # doesn't exist in our class4 relationships list
        with self.assertRaises(IndexError):
            class4.remove_relationship(class5.name)

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLClass.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLClass.py' command
if __name__ == '__main__':
    unittest.main()