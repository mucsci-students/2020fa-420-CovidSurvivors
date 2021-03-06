# A representation of a UML Relationship
# Description:     
#   This file holds all data that can be associated 
#   with a UML relationship
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

##########################################################################
# Imports 

from .RelationshipType import RelationshipType

##########################################################################

# Represents the relationship between 2 UML Classes 
class UMLRelationship:

    def __init__(self, _type:RelationshipType, other:str):
        """Represents a partial UML Relationship object with the given name 
        and given related-to UMLClass

        Params:
        - _type (RelationshipType) - the type for the relationship
        - other (string) - the name of the other class in the relationship
        """
        # Represents the Relationships name
        self.type = _type
        # The other class in the relationship
        self.other = other

    ######################################################################

    def get_raw_data(self):
        """Returns a JSON convertible form of the data"""
        return {"type" : RelationshipType.to_string(self.type), 
                "other" : self.other
                }

##########################################################################

    @staticmethod
    def from_raw_data(data):
        """Constructs a UMLRelationship object from a set of data
        
        Precondition:
        - The data should have been generated by a call to get_raw_data()
        """
        return UMLRelationship(RelationshipType.from_string(data["type"]), data["other"])

##########################################################################
