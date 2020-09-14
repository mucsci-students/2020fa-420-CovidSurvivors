# A representation of the state of a UML Model
# Description:     
#   This file keeps track of all the classes that are in the UML Model
#   It also handles saving/loading the Model to/from a JSON file 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 13 2020

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

    # Outputs all classes in the model 
    def list_classes(self):
        for class_name in self.classes:
            print (class_name)

    ######################################################################

    # Outputs all attributes for a given class
    def list_attributes(self, class_name:str):
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

    # Outputs all of the relationships for a given class 
    # if class is not specified, all relationships are listed
    def list_relationships(self, class_name:str = ""):
        # list relationships for a specific class
        if class_name != "":
            # ensure class exists
            if class_name in self.classes:
                print (f"Relationships for {class_name}")
                # list all relationships for the class
                for relationship in self.classes[class_name].relationships:
                    if relationship.class1.name == class_name:
                        print (class_name,"---", relationship.name, "-->",relationship.class2.name)
                    else: 
                        print (class_name,"---", relationship.name, "-->",relationship.class1.name)

            # class_name is invalid
            else: 
                print (f"{class_name} does not exist")
        # list all relationships
        else:
            # for each class
            for class_name in self.classes:
                # for each relationship
                for relationship in self.classes[class_name].relationships:
                    # determine which class is the other 
                    if relationship.class1.name == class_name:
                        print (class_name,"---", relationship.name, "-->",relationship.class2.name)
                    else: 
                        print (class_name,"---", relationship.name, "-->",relationship.class1.name)

##########################################################################

