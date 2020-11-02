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

##########################################################################

# Unit test for the UMLMethod
class TestUMLClass(unittest.TestCase):
    
    # validates intended behavior of rename method
    def test_rename(self):
        # create method object
        method1 = UMLMethod("public", "run", "void")
        # make sure the initialized name is correct
        self.assertTrue(method1.name == "run")
        # rename the method object
        method1.rename("walk")
        # test whether or not the name changed
        self.assertTrue(method1.name == "walk")

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLMethod.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLMethod.py' command
if __name__ == '__main__':
    unittest.main()