# Unit test for the Variable class
# Description:     
#   This file validates that each function belonging to the Variable class behaves as intended
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
from models.Variable import Variable

##########################################################################

# Unit test for the Variable
class TestVarialbe(unittest.TestCase):
    
    # validates intended behavior of rename variable 
    def test_rename(self):
        # create variable object
        testVariable = Variable("varType", "varName")
        # ensure the initialized name is correct
        self.assertTrue(testVariable.name == "varName")
        # rename the variable object
        testVariable.rename("fakeVarName")
        # test whether or not the name changed
        self.assertTrue(testVariable.name == "fakeVarName")

##########################################################################

    # validates intended behavior of set_type variable 
    def test_set_type(self):
        # create variable object
        testVariable = Variable("varType", "varName")
        # ensure the initialized type is correct
        self.assertTrue(testVariable.type == "varType")
        # change the type of the variable object
        testVariable.set_type("void")
        # test whether or not the type changed
        self.assertTrue(testVariable.type == "void")

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_Variable.py' command
# without it, we would have to use the 'python3 -m unittest test_Variable.py' command
if __name__ == '__main__':
    unittest.main()