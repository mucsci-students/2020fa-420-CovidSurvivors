# Unit test for the UMLField
# Description:     
#   This file validates that each function belonging to the UMLField class behaves as intended
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
from models.UMLField import UMLField

##########################################################################

# Unit test for the UMLField
class TestUMLField(unittest.TestCase):
    
    # validates intended behavior of rename field (from variable.py)
    def test_rename(self):
        # create field object
        testField = UMLField("private", "fName", "string")
        # ensure the initialized name is correct
        self.assertTrue(testField.name == "fName")
        # rename the field object
        testField.rename("lName")
        # test whether or not the name changed
        self.assertTrue(testField.name == "lName")

##########################################################################

    # validates intended behavior of set_type field (from variable.py)
    def test_set_type(self):
        # create field object
        testField = UMLField("private", "fName", "string")
        # ensure the initialized type is correct
        self.assertTrue(testField.type == "string")
        # change the type of the field object
        testField.set_type("int")
        # test whether or not the type changed
        self.assertTrue(testField.type == "int")

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLField.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLField.py' command
if __name__ == '__main__':
    unittest.main()