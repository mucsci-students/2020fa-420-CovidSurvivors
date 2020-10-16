# Unit test for the UMLClass
# Description:     
#   This file validates that each function belonging to the UMLField class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 11, 2020

##########################################################################
# Imports

import unittest
import sys
sys.path.append('../')
from models.UMLField import UMLField

##########################################################################

# Unit test for the UMLField
class TestUMLField(unittest.TestCase):
    
    # validates intended behavior of rename field
    def test_rename(self):
        # create field object
        field1 = UMLField("private", "fName", "string")
        # make sure the initialized name is correct
        self.assertTrue(field1.name == "fName")
        # rename the field object
        field1.rename("lName")
        # test whether or not the name changed
        self.assertTrue(field1.name == "lName")

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLField.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLField.py' command
if __name__ == '__main__':
    unittest.main()