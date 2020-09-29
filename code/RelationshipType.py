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