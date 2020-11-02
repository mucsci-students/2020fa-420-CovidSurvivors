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
    R_INHERITANCE = 2
    REALIZATION = 3
    R_REALIZATION = 4
    COMPOSITION = 5
    R_COMPOSITION = 6
    AGGREGATION = 7
    R_AGGREGATION = 8
    INVALID = 9

##########################################################################

    def from_string(t:str):
        """Converts a string to a relationship type
        RelationshipType.INVALID is returned if string does not match
        """
        if t == "inheritance":
            return RelationshipType.INHERITANCE
        if t == "reverse inheritance":
            return RelationshipType.R_INHERITANCE
        if t == "realization":
            return RelationshipType.REALIZATION
        if t == "reverse realization":
            return RelationshipType.R_REALIZATION
        if t == "composition":
            return RelationshipType.COMPOSITION
        if t == "reverse composition":
            return RelationshipType.R_COMPOSITION
        if t == "aggregation":
            return RelationshipType.AGGREGATION
        if t == "reverse aggregation":
            return RelationshipType.R_AGGREGATION
        return RelationshipType.INVALID 

##########################################################################

    def to_string(rtype):
        """Converts a relationship type to a string
        "" is returned if the type is invalid
        """
        if rtype == RelationshipType.INHERITANCE:
            return "inheritance"
        if rtype == RelationshipType.R_INHERITANCE:
            return "reverse inheritance"
        if rtype == RelationshipType.REALIZATION:
            return "realization"
        if rtype == RelationshipType.R_REALIZATION:
            return "reverse realization"
        if rtype == RelationshipType.COMPOSITION:
            return "composition"
        if rtype == RelationshipType.R_COMPOSITION:
            return "reverse composition"
        if rtype == RelationshipType.AGGREGATION:
            return "aggregation"
        if rtype == RelationshipType.R_AGGREGATION:
            return "reverse aggregation"
        return ""

##########################################################################

    def to_arrow(rtype):
        """Converts a relationship type to
        a corresponding string arrow
        """
        if rtype == RelationshipType.INHERITANCE:
            return "--------->"
        if rtype == RelationshipType.R_INHERITANCE:
            return "<---------"
        if rtype == RelationshipType.REALIZATION:
            return "- - - - ->"
        if rtype == RelationshipType.R_REALIZATION:
            return "<- - - - -"
        if rtype == RelationshipType.COMPOSITION:
            return "--------<>"
        if rtype == RelationshipType.R_COMPOSITION:
            return "<>--------"
        if rtype == RelationshipType.AGGREGATION:
            return "------<<>>"
        if rtype == RelationshipType.R_AGGREGATION:
            return "<<>>------"