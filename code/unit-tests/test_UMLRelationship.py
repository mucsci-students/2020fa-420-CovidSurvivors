# Unit test for the UMLRelationship
# Description:     
#   This file validates that each function belonging to the UMLRelationship class behaves as intended
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
from models.UMLRelationship import UMLRelationship
from models.RelationshipType import RelationshipType

##########################################################################

# Unit test for the UMLRelationship
class TestUMLRelationship(unittest.TestCase):

    # validates intended behavior of get_raw_data method
    def test_get_raw_data(self):
        # create relationship of type realization
        testRelationshipReal = UMLRelationship(RelationshipType.from_string("realization"), "class1")
        # create relationship of type aggregation
        testRelationshipAgg = UMLRelationship(RelationshipType.from_string("aggregation"), "class2")

        # expected relationship data for testRelationshipReal
        real = {
            "type" : "realization",
            "other" : "class1"
        }
        # expected relationship data for testRelationshipAgg
        agg = {
            "type" : "aggregation",
            "other" : "class2"
        }

        # ensure the JSON convertible form of the data outputs the correct data
        self.assertEqual(testRelationshipReal.get_raw_data(), real)
        self.assertEqual(testRelationshipAgg.get_raw_data(), agg)
    
##########################################################################

    # validates intended behavior of from_raw_data method
    def test_from_raw_data(self):
        # create relationship of type realization
        testRelationshipReal = UMLRelationship(RelationshipType.from_string("realization"), "class1")
        # create relationship of type aggregation
        testRelationshipAgg = UMLRelationship(RelationshipType.from_string("aggregation"), "class2")

        # generate relationship data
        real = testRelationshipReal.get_raw_data()
        agg = testRelationshipAgg.get_raw_data()

        # ensure that a UMLRelationship object is constructed from the relationship data
        self.assertTrue(isinstance(testRelationshipReal.from_raw_data(real), object))
        self.assertTrue(isinstance(testRelationshipAgg.from_raw_data(agg), object))

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLMethod.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLMethod.py' command
if __name__ == '__main__':
    unittest.main()