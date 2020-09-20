# A representation of a UML Class
# Description:     
#   This file holds all data that can be associated with a UML Class
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 8 2020

##########################################################################
# Imports 

##########################################################################

# Representation of a UML Class 
class UMLClass:

    # Constructs a UML Class object with a given name and initially 
    #    has no attributes or relationships 
    # @param name - the name for the UML Class
    def __init__(self, name:str):
        # Represents this classes name
        self.name = name
        # A list of all attributes that belong to this class
        self.attributes = []
        # A list of all relationships that this class participates in 
        self.relationships = []

##########################################################################

    # Adds an attribute to this class
    # @param attribute - an attribute name to add to the class
    # @precondition - attribute should not already exist
    # @postcondition - attribute will be added to the list
    #   of attributes 
    def add_attribute(self, attribute:str):
        self.attributes += [attribute]

##########################################################################  
    
    # Removes an attribute to this class
    # @param attribute - an attribute name to remove from the class
    # @precondition - attribute should exist
    # @postcondition - attribute will be removed from the list of 
    #   attributes 
    def remove_attribute(self, attribute:str):
        self.attributes.remove(attribute) 

##########################################################################   

    # Adds a relationship object to this class
    # @param relationship - a relationship to add to the class
    # @precondition - relationship should not already exist
    # @postcondition - relationship will be added to the list of 
    #   relationships 
    def add_relationship(self, relationship):
         self.relationships += [relationship]

##########################################################################

    # Removes a relationship object from this class
    # @param relationship - a relationship to remove from the class
    # @precondition - relationship should exist
    # @postcondition - relationship will be removed from the list of 
    #   relationships
    def remove_relationship(self, relationship):
        self.relationships.remove(relationship)      

##########################################################################
