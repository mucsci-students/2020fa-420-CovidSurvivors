# A representation of a UML Relationship
# Description:     
#   This file holds all data that can be associated 
#   with a UML relationship
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

##########################################################################
# Imports 

from RelationshipType import RelationshipType

##########################################################################

# Represents the relationship between 2 UML Classes 
class UMLRelationship:

    def __init__(self, _type:RelationshipType, class1, class2):
        """Constructs a UML Relationship object with the given type 
        and given UMLClasses

        Params:
        - _type (RelationshipType) - the type of the relationship
        - class1 (UMLClass) - the first class in the relationship
        - class2 (UMLClass) - the second class in the relationship
        """
        # Represents the Relationship's type
        self.type = _type
        # The first class participating in the relationship
        self.class1 = class1
        # The second class participating in the relationship
        self.class2 = class2
        # Used in saving/loading to key track of unique relationships
        self.tag = -1

    ######################################################################

    def get_other_class(self, class_name:str):
        """Returns the opposite class of the given

        Params:
        - class_name (string) - the name of the class

        Precondition:
        - class_name must be a name of either class

        """
        if class_name == self.class1.name:
            return self.class2
        return self.class1 

    ######################################################################

##########################################################################