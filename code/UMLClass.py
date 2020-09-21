# A representation of a UML Class
# Description:     
#   This file holds all data that can be associated with a UML Class
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

##########################################################################
# Imports 

##########################################################################

class UMLClass:
    """A representation of a UML Class"""

    def __init__(self, name:str):
        """Constructs a UML Class object with a given name and
        has no attributes or relationships 
        
        Params:
        - name (string) - the name for the class
        """
        # Represents this classes name
        self.name = name
        # A list of all attributes that belong to this class
        self.attributes = []
        # A list of all relationships that this class participates in 
        self.relationships = []

##########################################################################

    def add_attribute(self, attribute:str):
        """Adds an attribute to this class

        Params:
        - attribute (string) - the name for an attribute to add

        Preconditions:
        - attribute should not already exist

        Postconditions:
        - attribute will be added to the list of attributes
        """
        self.attributes += [attribute]

##########################################################################  
    
    def remove_attribute(self, attribute:str):
        """Deletes an attribute from this class

        Params:
        - attribute (string) - the name for an attribute to delete

        Preconditions:
        - attribute should exist

        Postconditions:
        - attribute will be deleted from the list of attributes
        """
        self.attributes.remove(attribute) 

##########################################################################   

    def add_relationship(self, relationship):
        """Adds a relationship object to this class

        Params:
        - relationship (UMLRelationship) - a relationship to add

        Precondition:
        - relationship should not already exist

        Postcondition:
        - relationship will be added to the list of relationships
        """
        self.relationships += [relationship]

##########################################################################

    def remove_relationship(self, relationship):
        """Removes a relationship object from this class

        Params:
        - relationship (UMLRelationship) - a relationship to remove

        Precondition:
        - relationship should exist

        Postcondition:
        - relationship will be removed from the list of relationships
        """
        self.relationships.remove(relationship)      

##########################################################################
