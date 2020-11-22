# Unit test for the UMLMethod
# Description:     
#   This file validates that each function belonging to the UMLMethod class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 11, 2020

##########################################################################
# Imports

import unittest
import pytest
import sys
sys.path.append('../')
sys.path.append('code/')
from models.UMLMethod import UMLMethod
from models.Visibility import Visibility

##########################################################################

# Unit test for the UMLMethod
class TestUMLMethod(unittest.TestCase):
    
    # validates intended behavior of rename method (from variable.py)
    def test_rename(self):
        # create method object
        testMethod = UMLMethod("public", "run", "void")
        # ensure the initialized name is correct
        self.assertTrue(testMethod.name == "run")
        # rename the method object
        testMethod.rename("walk")
        # test whether or not the name changed
        self.assertTrue(testMethod.name == "walk")

##########################################################################

    # validates intended behavior of set_type method (from variable.py)
    def test_set_type(self):
        # create method object
        testMethod = UMLMethod("public", "run", "void")
        # ensure the initialized type is correct
        self.assertTrue(testMethod.type == "void")
        # change the type of the method object
        testMethod.set_type("int")
        # test whether or not the type changed
        self.assertTrue(testMethod.type == "int")

##########################################################################

    # validates intended behavior of create_parameter method
    def test_create_parameter(self):
        # create method object
        testMethod = UMLMethod("private", "walk", "void")
        # ensure the method object has no parameters
        self.assertFalse(testMethod.has_parameter("speed"))
        # add parameter "speed" to the method
        testMethod.create_parameter("double", "speed")
        # ensure the method has parameter "speed"
        self.assertTrue(testMethod.has_parameter("speed"))

##########################################################################

    # validates intended behavior of rename_parameter method
    def test_rename_parameter(self):
        # create method object
        testMethod = UMLMethod("private", "walk", "void")
        # add parameter "speed" to the method
        testMethod.create_parameter("double", "speed")
        # rename parameter "speed" to "distance"
        testMethod.rename_parameter("speed", "distance")
        # ensure the parameter "speed" has been rename to "distance"
        self.assertTrue(testMethod.has_parameter("distance"))

##########################################################################

    # validates intended behavior of delete_parameter method
    def test_delete_parameter(self):
        # create method object
        testMethod = UMLMethod("private", "walk", "void")
        # add parameter "speed" to the method
        testMethod.create_parameter("double", "speed")
        # ensure the method has parameter "speed"
        self.assertTrue(testMethod.has_parameter("speed"))
        # delete parameter "speed"
        testMethod.delete_parameter("speed")
        # ensure the parameter "speed" has been deleted
        self.assertFalse(testMethod.has_parameter("speed"))

##########################################################################

    # validates intended behavior of parameter_index method
    def test_parameter_index(self):
        # create method object
        testMethod = UMLMethod("private", "walk", "void")
        # add parameter "acceleration" to the method
        testMethod.create_parameter("double", "acceleration")
        # add parameter "speed" to the method
        testMethod.create_parameter("double", "speed")
        # add parameter "distance" to the method
        testMethod.create_parameter("double", "distance")
        # ensure the parameters are in the correct indices
        self.assertEqual(testMethod.parameter_index("acceleration"), 0)
        self.assertEqual(testMethod.parameter_index("speed"), 1)
        self.assertEqual(testMethod.parameter_index("distance"), 2)

##########################################################################

    # validates intended behavior of get_raw_data method
    def test_get_raw_data(self):
        # create method object
        testMethod = UMLMethod(Visibility.from_string("private"), "walk", "void")
        # add parameter "speed" to the method
        testMethod.create_parameter("int", "speed")
        # add parameter "distance" to the method
        testMethod.create_parameter("double", "distance")
        # add parameter "acceleration" to the method
        testMethod.create_parameter("double", "acceleration")
        # expected method data
        data = {
                "visibility": "private",
                "name": "walk",
                "type": "void",
                "parameters": [
                    {
                        "type": "int",
                        "name": "speed"
                    },
                    {
                        "type": "double",
                        "name": "distance"
                    },
                    {
                        "type": "double",
                        "name": "acceleration"
                    }
                ]
            }
        # ensure the JSON convertible form of the data outputs the correct data
        self.assertEqual(testMethod.get_raw_data(), data)
   
##########################################################################

    # validates intended behavior of from_raw_data method
    def test_from_raw_data(self):
        # create method object
        testMethod = UMLMethod(Visibility.from_string("private"), "walk", "void")
        # add parameter "speed" to the method
        testMethod.create_parameter("double", "speed")
        # add parameter "distance" to the method
        testMethod.create_parameter("double", "distance")
        # add parameter "acceleration" to the method
        testMethod.create_parameter("double", "acceleration")
        # generate method data
        data = testMethod.get_raw_data()
        # ensure that a UMLMethod object is constructed from the method data
        self.assertTrue(isinstance(testMethod.from_raw_data(data), object))
        
##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLMethod.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLMethod.py' command
if __name__ == '__main__':
    unittest.main()