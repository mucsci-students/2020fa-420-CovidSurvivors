# A representation of a UML Relationship
# Description:     
#   This file holds all data that can be associated 
#   with a UML relationship
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 8 2020

##########################################################################
# Imports 

##########################################################################

# Represents the relationship between 2 UML Classes 
class UMLRelationship:

    # Constructs a UML Relationship object with the 
    # given name and given UML classes 
    # @param name - the name/title for the relationship
    # @param class1 - a class that is participating in the relationship
    # @param class2 - a class that is participating in the relationship
    # @precondition - class1 and class2 are UMLClass objects that have
    #   been initialized
    # @postcondition - a relationship is constructed with the given params 
    def __init__(self, name:str, class1, class2):
        # Represents the Relationships name
        self.name = name
        # The first class participating in the relationship
        self.class1 = class1
        # The second class participating in the relationship
        self.class2 = class2

    ######################################################################

##########################################################################