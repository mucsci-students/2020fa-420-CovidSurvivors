# Unit test for the Visibility
# Description:     
#   This file validates that each function belonging to the Visibility class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     November 22, 2020

##########################################################################
# Imports

import unittest
import pytest
import sys
sys.path.append('../')
sys.path.append('code/')
from models.Visibility import Visibility

##########################################################################

# Unit test for the Visibility
class TestVisibility(unittest.TestCase):

    # validates intended behavior of from_string method
    def test_from_string(self):
        # Ensure the string is converted to the appropriate visibility type
        self.assertEqual(str(Visibility.from_string("public")), "Visibility.PUBLIC")
        self.assertEqual(str(Visibility.from_string("private")), "Visibility.PRIVATE")
        self.assertEqual(str(Visibility.from_string("protected")), "Visibility.PROTECTED")
        self.assertEqual(str(Visibility.from_string("invalidVisibility")), "Visibility.INVALID")
        
    # validates intended behavior of to_string method
    def test_to_string(self):
        # Ensure the visibility type is converted to the appropriate string representation of the visibility type
        self.assertEqual(Visibility.to_string(Visibility.from_string("public")), "public")
        self.assertEqual(Visibility.to_string(Visibility.from_string("private")), "private")
        self.assertEqual(Visibility.to_string(Visibility.from_string("protected")), "protected")
        self.assertEqual(Visibility.to_string(Visibility.from_string("invalidRelationshipType")), "invalid")

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLMethod.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLMethod.py' command
if __name__ == '__main__':
    unittest.main()