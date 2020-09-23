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

    def __init__(self, name:str):
        """Constructs a UML Class object with a given name and
        has no attributes or relationships by default
        
        Params:
        - name (string) - the name for the class
        """
        # Represents this classes name
        self.name = name
        # A list of all attributes that belong to this class
        self.attributes = []
        # A dictionary of all relationships that this class 
        # participates in 
        # map of (other_class_name, relationship)
        self.relationships = {}

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
    
    def has_attribute(self, attribute:str):
        """Returns true if attribute exists, false otherwise

        Params:
        - attribute (string) - the name for an attribute

        """
        return attribute in self.attributes

##########################################################################   

    def add_relationship(self, other_class_name, relationship):
        """Adds a relationship object to this class

        NOTE:
        - You must add the relationship to the other class. This function 
        only adds the relationship to this class.

        Params:
        - other_class_name (string) - the name of the class to relate to
        - relationship (UMLRelationship) - a relationship to add

        Precondition:
        - relationship should not already exist

        Postcondition:
        - relationship will be added to the dictionary of relationships
        """
        self.relationships[other_class_name] = relationship

##########################################################################

    def remove_relationship(self, other_class_name):
        """Removes a relationship object from this class

        NOTE: 
        - You are responsible for deleting the relationship from
         other classes.

        Params:
        - other_class_name (string) - the name of the class to disassociate

        Precondition:
        - relationship should exist

        Postcondition:
        - relationship will be removed from the dictionary of relationships
        """
        del self.relationships[other_class_name]  


##########################################################################   

    def has_relationship(self, other_class_name):
        """Returns true if a relationship to the given class exists,
        Otherwise false 

        Params:
        - other_class_name (string) - the name of the other class 
        """
        return other_class_name in self.relationships

##########################################################################
