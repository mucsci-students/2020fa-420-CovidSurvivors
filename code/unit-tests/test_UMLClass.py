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
sys.path.append('code/')
from models.UMLClass import UMLClass
from models.UMLRelationship import UMLRelationship

##########################################################################

# Unit test for the UMLClass
class TestUMLClass(unittest.TestCase):
    
    # validates intended behavior of add_field method
    def test_add_field(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')
        # test to see if the name of our class is 'testClass'
        self.assertEqual(testClass.name, 'testClass')

        # we haven't added any fields to testClass
        # check to see if the field list for testClass is empty
        self.assertEqual(testClass.fields, [])

        # add a field to testClass
        testClass.add_field('public', 'A', 'string')
        # check to see if the field we added are in our testClass fields list
        self.assertTrue(testClass.has_field('A'))

        # add two additional fields to testClass
        testClass.add_field('private', 'B', 'string')
        testClass.add_field('private', 'C', 'string')
        # check to see if the fields we added are in our testClass fields list
        self.assertTrue(testClass.has_field('B'))
        self.assertTrue(testClass.has_field('C'))

    ##########################################################################

    # validates intended behavior of rename_field method
    def test_rename_field(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')

        # add two fields to testClass
        testClass.add_field('public', 'A', 'string')
        testClass.add_field('private', 'B', 'int')

        # rename the fields
        testClass.rename_field('A', 'C')
        testClass.rename_field('B', 'D')

        # check to see if the fields we renamed are in our testClass fields list
        self.assertTrue(testClass.has_field('C'))
        self.assertTrue(testClass.has_field('D'))

    ##########################################################################

    # validates intended behavior of remove_field method
    def test_remove_field(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')

        # check to see that an exception is raised if the user tries to remove an field from
        # the class when no fields have been added to the fields list
        with self.assertRaises(IndexError):
            testClass.remove_field('D')

        # add some fields to testClass
        testClass.add_field('public', 'D', 'enum')
        testClass.add_field('private', 'E', 'double')
        testClass.add_field('private', 'F', 'array')
        testClass.add_field('public', 'G', 'int')
        # check to see if the fields we added are in our testClass fields list
        self.assertTrue(testClass.has_field('D'))
        self.assertTrue(testClass.has_field('E'))
        self.assertTrue(testClass.has_field('F'))
        self.assertTrue(testClass.has_field('G'))

        # remove an existing field from testClass
        testClass.remove_field('G')
        # check to see if the field we removed has been removed from our testClass fields list
        self.assertFalse(testClass.has_field('G'))

        # remove another field from testClass
        testClass.remove_field('E')
        # check to see if the field we removed has been removed from our testClass fields list
        self.assertFalse(testClass.has_field('E'))

    ##########################################################################

    # validates intended behavior of add_method method
    def test_add_method(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')
        # test to see if the name of our class is 'testClass'
        self.assertEqual(testClass.name, 'testClass')

        # we haven't added any methods to testClass
        # check to see if the method list for testClass is empty
        self.assertEqual(testClass.methods, [])

        # add an method to testClass
        testClass.add_method('public', 'A', 'string')
        # check to see if the method we added are in our testClass methods list
        self.assertTrue(testClass.has_method('A'))

        # add two additional methods to testClass
        testClass.add_method('private', 'B', 'string')
        testClass.add_method('private', 'C', 'string')
        # check to see if the methods we added are in our testClass methods list
        self.assertTrue(testClass.has_method('B'))
        self.assertTrue(testClass.has_method('C'))

    ##########################################################################

    # validates intended behavior of rename_method method
    def test_rename_method(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')

        # add two methods to testClass
        testClass.add_method('public', 'walk', 'string')
        testClass.add_method('private', 'run', 'int')

        # rename the methods
        testClass.rename_method('walk', 'stroll')
        testClass.rename_method('run', 'jog')

        # check to see if the methods we renamed are in our testClass methods list
        self.assertTrue(testClass.has_method('stroll'))
        self.assertTrue(testClass.has_method('jog'))

    ##########################################################################

    # validates intended behavior of remove_method method
    def test_remove_method(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')

        # check to see that an exception is raised if the user tries to remove an method from
        # the class when no methods have been added to the methods list
        with self.assertRaises(IndexError):
            testClass.remove_method('D')

        # add some methods to testClass
        testClass.add_method('public', 'D', 'enum')
        testClass.add_method('private', 'E', 'double')
        testClass.add_method('private', 'F', 'array')
        testClass.add_method('public', 'G', 'int')
        # check to see if the methods we added are in our testClass methods list
        self.assertTrue(testClass.has_method('D'))
        self.assertTrue(testClass.has_method('E'))
        self.assertTrue(testClass.has_method('F'))
        self.assertTrue(testClass.has_method('G'))

        # remove an existing method from testClass
        testClass.remove_method('G')
        # check to see if the method we removed has been removed from our testClass methods list
        self.assertFalse(testClass.has_method('G'))

        # remove another method from testClass
        testClass.remove_method('E')
        # check to see if the method we removed has been removed from our testClass methods list
        self.assertFalse(testClass.has_method('E'))

    ##########################################################################

    # validates intended behavior of create_parameter method
    def test_create_parameter(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')

        # add a method to testClass
        testClass.add_method('public', 'run', 'void')
        
        # add parameters to 'run' method
        testClass.create_parameter('run', 'double', 'speed')
        testClass.create_parameter('run', 'double', 'distance')

        # ensure the method object has the parameters
        self.assertTrue(testClass.methods[0].has_parameter('speed'))
        self.assertTrue(testClass.methods[0].has_parameter('distance'))

    ##########################################################################

    # validates intended behavior of rename_parameter method
    def test_rename_parameter(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')

        # add a method to testClass
        testClass.add_method('public', 'run', 'void')
        
        # add parameters to 'run' method
        testClass.create_parameter('run', 'double', 'speed')
        testClass.create_parameter('run', 'double', 'distance')
        
        # rename the parameters
        testClass.rename_parameter('run', 'speed', 'resistance')
        testClass.rename_parameter('run', 'distance', 'direction')

        # ensure the method object has the parameters
        self.assertTrue(testClass.methods[0].has_parameter('resistance'))
        self.assertTrue(testClass.methods[0].has_parameter('direction'))


    ##########################################################################

    # validates intended behavior of create_parameter method
    def test_delete_parameter(self):
        # create a new class called testClass
        testClass = UMLClass('testClass')

        # add a method to testClass
        testClass.add_method('public', 'run', 'void')
        
        # add parameters to 'run' method
        testClass.create_parameter('run', 'double', 'speed')
        testClass.create_parameter('run', 'double', 'distance')

        # ensure the method object has the parameters
        self.assertTrue(testClass.methods[0].has_parameter('speed'))
        self.assertTrue(testClass.methods[0].has_parameter('distance'))

        # delete one of the parameters
        testClass.delete_parameter('run', 'speed')

        # ensure the parameter 'speed' has been deleted
        self.assertFalse(testClass.methods[0].has_parameter('speed'))

    ##########################################################################

    # validates intended behavior of add_relationship method
    def test_add_relationship(self):
        # create a new class called classOne
        classOne = UMLClass('classOne')
        classTwo = UMLClass('classTwo')
        classThree = UMLClass('classThree')

        # we haven't added any relationips to classOne
        # check to see if the relationships list for classOne is empty
        self.assertEqual(len(classOne.relationships), 0)
        self.assertEqual(len(classTwo.relationships), 0)
        self.assertEqual(len(classThree.relationships), 0)

        # add some relationships to our classes
        classOne.add_relationship("inheritance", classThree)
        classTwo.add_relationship("composition", classOne)
        classThree.add_relationship("aggregation", classTwo)        
        

        # check to see if the relationships we added are in our relationships lists
        self.assertTrue(classOne.relationships != [])
        self.assertTrue(classTwo.relationships != [])
        self.assertTrue(classThree.relationships != [])

    ##########################################################################

    # validates intended behavior of remove_relationship method
    def test_remove_relationship(self):
        # create a new class called classTwo
        classOne = UMLClass('classOne')
        classTwo = UMLClass('classTwo')
        classThree = UMLClass('classThree')

        # add some relationships to our classes
        classOne.add_relationship("inheritance", classThree)
        classTwo.add_relationship("composition", classOne)
        classThree.add_relationship("aggregation", classTwo)        

        # remove a relationship from classTwo
        classTwo.remove_relationship(classThree.name)
        classThree.remove_relationship(classTwo.name)
        # check to see if the relationship we removed was removed from our classTwo relationships list
        self.assertTrue(not classTwo.has_relationship(classThree.name))

        # remove the rest of the relationships from classTwo
        classOne.remove_relationship(classTwo.name)
        # check to see if the relationships we removed were removed from our classes relationships lists
        self.assertEqual(len(classOne.relationships), 0)
        
        # check to see that an exception is raised if the user tries to remove a relationsip that 
        # doesn't exist in our classTwo relationships list
        with self.assertRaises(IndexError):
            classTwo.remove_relationship(classThree.name)

##########################################################################

    # validates intended behavior of relationship_index method
    def test_relationship_index(self):
        # create a new class called classOne
        classOne = UMLClass('classOne')
        classTwo = UMLClass('classTwo')
        classThree = UMLClass('classThree')

        # add some relationships to our classes
        classOne.add_relationship("inheritance", "classTwo")
        classOne.add_relationship("realization", "classThree")

        # ensure the relationships are in their proper positions
        self.assertEqual(classOne.relationship_index("classTwo"), 0)
        self.assertEqual(classOne.relationship_index("classThree"), 1)

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLClass.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLClass.py' command
if __name__ == '__main__':
    unittest.main()