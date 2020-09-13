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
    
    # **Write Documentation Here**
    def create_class(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def rename_class(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
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

    # Output all attributes for a given class
    def list_class(self, class_name:str):
        # Ensure class exists
        if class_name in self.classes:
            # loop the classes by the name 
            for i in range(len(self.classes[class_name].attributes)):
                attribute = self.classes[class_name].attributes[i]
                print(attribute)
        # not valid class
        else:
            print (f"{class_name} is not a class")

    ######################################################################

    # Output all of the relationships between classes
    def list_relationships(self):
        # for each class
        for class_name in self.classes:
            # for each relationship
            for j in range(len(self.classes[class_name].relationships)):
                # determine which class is the other 
                relationship = self.classes[class_name].relationships[j]
                if relationship.class1.name == class_name:
                    print (class_name,"->",relationship.class2.name)
                else: 
                    print (class_name,"->",relationship.class1.name)

##########################################################################

