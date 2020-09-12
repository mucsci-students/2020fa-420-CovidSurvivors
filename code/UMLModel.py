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
        # Checks to see if class already exists
        if name in self.classes:
            print("{} already exists.".format(name))
        else:
            # Creates class object and assigns it to a key
            self.classes[name] = UMLClass.UMLClass(name)

    ######################################################################
    
    # Renames an existing class object
    def rename_class(self, oldClassName:str, newClassName:str):
        # Checks if the old class name exists       
        if oldClassName not in self.classes:
            print("{} does not exist.".format(oldClassName))
        # Checks if the new class name is already in use 
        elif newClassName in self.classes:
            print("{} already exists.".format(newClassName))
        else:
            # Renames existing class object
            (self.classes[oldClassName]).name = newClassName
            # Assigns the renamed class object to a key with the new class name
            self.classes[newClassName] = self.classes.pop(oldClassName)

    ######################################################################
    
    # Deletes an existing class
    def delete_class(self, name:str):
        # Checks to see if specified class exists
        if name in self.classes:
            # Deletes key-value pair for specified class
            del self.classes[name]
        else:
            print("{} does not exist.".format(name))

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

