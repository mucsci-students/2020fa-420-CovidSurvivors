# Unit test for the RelationshipType
# Description:     
#   This file validates that each function belonging to the RelationshipType class behaves as intended
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
from models.RelationshipType import RelationshipType

##########################################################################

# Unit test for the RelationshipType
class TestRelationshipType(unittest.TestCase):

    # validates intended behavior of from_string method
    def test_from_string(self):

        # Ensure the string is converted to the appropriate relationship type
        self.assertEqual(str(RelationshipType.from_string("inheritance")), "RelationshipType.INHERITANCE")
        self.assertEqual(str(RelationshipType.from_string("reverse inheritance")), "RelationshipType.R_INHERITANCE")

        self.assertEqual(str(RelationshipType.from_string("realization")), "RelationshipType.REALIZATION")
        self.assertEqual(str(RelationshipType.from_string("reverse realization")), "RelationshipType.R_REALIZATION")
        
        self.assertEqual(str(RelationshipType.from_string("composition")), "RelationshipType.COMPOSITION")
        self.assertEqual(str(RelationshipType.from_string("reverse composition")), "RelationshipType.R_COMPOSITION")

        self.assertEqual(str(RelationshipType.from_string("aggregation")), "RelationshipType.AGGREGATION")
        self.assertEqual(str(RelationshipType.from_string("reverse aggregation")), "RelationshipType.R_AGGREGATION")

        self.assertEqual(str(RelationshipType.from_string("invalidRelationshipType")), "RelationshipType.INVALID")
        
    # validates intended behavior of to_string method
    def test_to_string(self):

        # Ensure the relationship type is converted to the appropriate string representation of the relationship type
        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("inheritance")), "inheritance")
        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("reverse inheritance")), "reverse inheritance")

        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("realization")), "realization")
        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("reverse realization")), "reverse realization")
       
        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("composition")), "composition")
        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("reverse composition")), "reverse composition")
        
        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("aggregation")), "aggregation")
        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("reverse aggregation")), "reverse aggregation")

        self.assertEqual(RelationshipType.to_string(RelationshipType.from_string("invalidRelationshipType")), "")

    # validates intended behavior of to_arrow method
    def test_to_arrow(self):

        # Ensure the relationship type is converted to the appropriate string arrow representation of the relationship type
        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("inheritance")), "--------->")
        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("reverse inheritance")), "<---------")

        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("realization")), "- - - - ->")
        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("reverse realization")), "<- - - - -")
       
        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("composition")), "--------<>")
        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("reverse composition")), "<>--------")
      
        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("aggregation")), "------<<>>")
        self.assertEqual(RelationshipType.to_arrow(RelationshipType.from_string("reverse aggregation")), "<<>>------")

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLMethod.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLMethod.py' command
if __name__ == '__main__':
    unittest.main()