# A representation of the state of a UML Model
# Description:     
#   This file keeps track of all the classes that are in the UML Model
#   It also handles saving/loading the Model to/from a JSON file 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 8 2020

##########################################################################
# Imports

import UMLClass
import UMLRelationship

##########################################################################

# Representation of a UML Model
class UMLModel:

    ######################################################################
    
    # Constructs an empty UML Model
    def __init__(self):
        
        # Dictionary mapping class names to their class object
        self.classes = {}

    ######################################################################
    
    # Creates class object
    def create_class(self, name:str):
        if name in self.classes:
            print("{} is already exists".format(name))
        else:
            self.classes[name] = UMLClass.UMLClass(name)
            
    ######################################################################
    
    # Assigns a new name to existing class object
    def rename_class(self):       
        print ("To be implemented")
            
    ######################################################################
    
    # Deletes an existing class
    def delete_class(self):
        print ("To be implemented")
        
    ######################################################################
    
    # **Write Documentation Here**
    def create_attribute(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def rename_attribute(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def delete_attribute(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def create_relationship(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def delete_relationship(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def save_model(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def load_model(self):
        print ("To be implemented")

    ######################################################################

    # **Write Documentation Here**
    def list_class(self):
        print ("To be implemented")

    ######################################################################

    # **Write Documentation Here**
    def list_relationships(self):
        print ("To be implemented")


##########################################################################

