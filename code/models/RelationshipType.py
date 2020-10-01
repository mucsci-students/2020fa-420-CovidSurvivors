# Simple Enum for a Relationship types 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 28 2020

##########################################################################
# Imports

from enum import Enum

##########################################################################

class RelationshipType(Enum):
    INHERITANCE = 1
    GENERALIZATION = 2
    COMPOSITION = 3
    AGGREGATION = 4
    INVALID = 5

##########################################################################

    @staticmethod
    def from_string(t:str):
        """Converts a string to a relationship type
        if 'inheritance' -> RelationshipType.INHERITANCE
        if 'generalization' -> RelationshipType.GENERALIZATION
        if 'composition' -> RelationshipType.COMPOSITION
        if 'aggregation' -> RelationshipType.AGGREGATION
        otherwise RelationshipType.INVALID is returned
        """
        if t == "inheritance":
            return RelationshipType.INHERITANCE
        if t == "generalization":
            return RelationshipType.GENERALIZATION
        if t == "composition":
            return RelationshipType.COMPOSITION
        if t == "aggregation":
            return RelationshipType.AGGREGATION
        return RelationshipType.INVALID 

##########################################################################

    @staticmethod
    def to_string(rtype):
        """Converts a relationship type to a string
        if RelationshipType.INHERITANCE -> 'inheritance'
        if RelationshipType.GENERALIZATION -> 'generalization'
        if RelationshipType.COMPOSITION -> 'composition'
        if RelationshipType.AGGREGATION -> 'aggregation'
        otherwise "" is returned
        """
        if rtype == RelationshipType.INHERITANCE:
            return "inheritance"
        if rtype == RelationshipType.GENERALIZATION:
            return "generalization"
        if rtype == RelationshipType.COMPOSITION:
            return "composition"
        if rtype == RelationshipType.AGGREGATION:
            return "aggregation"
        return ""