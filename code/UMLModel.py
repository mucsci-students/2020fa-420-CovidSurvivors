# A representation of the state of a UML Model
# Description:     
#   This file keeps track of all the classes that are in the UML Model
#   It also handles saving/loading the Model to/from a JSON file 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

##########################################################################
# Imports

import UMLClass
import UMLRelationship
import json
import os.path
from os import path

##########################################################################
# Constants 

# The directory where models are saved
MODEL_DIRECTORY = "models/"

##########################################################################

class UMLModel:

    """
    UMLModel

    A represenation of a UML Model which features classes that can have 
    attributes and relationships to other classes. 

    """

    ######################################################################
    
    def __init__(self):
        """Constructs an empty UMLModel"""
        # Dictionary mapping class names to their class object
        self.classes = {}

    ######################################################################
    
    def create_class(self, name:str):
        """Creates UML Class object and adds it to the model
            - name (string) - the name for the new class
        """
        # Checks to see if class already exists
        if name in self.classes:
            print("{} already exists.".format(name))
        else:
            # Creates class object and assigns it to a key
            self.classes[name] = UMLClass.UMLClass(name)

    ######################################################################
    
    def rename_class(self, oldClassName:str, newClassName:str):
        """Renames an existing UML Class 
            oldClassName (string) - name of class to rename
            newClassName (string) - new name for the class
        """
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
    
    def delete_class(self, name:str):
        """Deletes UML Class object from the model
            - name (string) - the name of the class to delete
        """
        # Checks to see if specified class exists
        if name in self.classes:
            # Deletes key-value pair for specified class
            del self.classes[name]
            print("{} has been deleted.".format(name))
        else:
            print("{} does not exist.".format(name))

    ######################################################################
    
    def create_attribute(self, class_name:str, attribute_name:str):
        """Creates an attribute for a given class
            - class_name (string) - the name of the class to add the 
                attribute to 
            - attribute_name (string) - the name for an attribute to 
                create and add to the class
        """
        # checks if the the class exists
        if class_name in self.classes:
            # checks if the class does not have an attribute with the same name inputted
            if attribute_name not in self.classes[class_name].attributes:
                # creates attribute in class
                self.classes[class_name].add_attribute(attribute_name)
                print("attribute {} has been created in {}".format(attribute_name, class_name))
            else:
                print("{} already exists in {}".format(attribute_name, class_name))   
        else:
            print("{} does not exist.".format(class_name))

    
    ######################################################################

    def find_attribute(self, class_name:str, attribute_name:str):
        """Gives the index of a given attribute in a given class

            If attribute does not exist, then -1 is returned 

            - class_name (string) - the name of the class
            - attribute_name (string) - the name of the attribute 
        """
        for i in range(len(self.classes[class_name].attributes)):
            # Finds the attribute 
            if self.classes[class_name].attributes[i] == attribute_name:
                return i
        return -1    

    ######################################################################
    
    def rename_attribute(self, class_name:str, old_attr_name:str, new_attr_name:str):
        """Renames an attribute for a given class
            - class_name (string) - the name of the class
            - old_attr_name (string) - the name of the attribute to rename
            - new_attr_name (string) - the new name of the attribute
        """
        # checks if the class exists
        if class_name not in self.classes:
            print("{} does not exist.".format(class_name))
            return

        # checks if the attribute exists in the class
        if not self.classes[class_name].has_attribute(old_attr_name):
            print("{} does not exist in {}.".format(old_attr_name, class_name))
            return
        
        # checks if the inputted new attribute name already exists in the class
        if self.classes[class_name].has_attribute(new_attr_name):  
            print("{} already exists in {}".format(new_attr_name, class_name))
            return
                
        # renames the attribute to new_attr_name
        index = self.find_attribute(class_name, old_attr_name)
        self.classes[class_name].attributes[index] = new_attr_name
        print("attribute {} has been renamed to {}".format(old_attr_name, new_attr_name))

    ######################################################################
    
    def delete_attribute(self, class_name:str, attribute_name:str):
        """Deletes a given attribute for a given class
            - class_name (string) - the name of the class
            - attribute_name (string) - the name for an attribute to 
                delete
        """
        # Ensure class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return 

        # Ensure attribute exists 
        if not self.classes[class_name].has_attribute(attribute_name):
            print(f"{attribute_name} is not an attribute of {class_name}")

        
        # Delete the attribute
        self.classes[class_name].remove_attribute(attribute_name)

        # Give user verification that attribute was deleted
        print("{} has been deleted from {}".format(attribute_name, class_name))

    ######################################################################
    
    def create_relationship(self, relationship_name:str, class_name1:str, class_name2:str):
        """Creates a relationship between two given classes
            - relationship_name (string) - the name of the relationship
            - class_name1 (string) - the name of the first class
            - class_name2 (string) - the name of the second class
        """
        # Ensure first class exists
        if class_name1 not in self.classes:
            print (f"{class_name1} does not exist")
            return
        # Ensure second class exists
        if class_name2 not in self.classes:
            print (f"{class_name2} does not exist")
            return 

        # Ensure relationship does not already exist
        # we only have to check one of the classes
        if self.classes[class_name1].has_relationship(class_name2):
            print(f"Relationship between {class_name1} and {class_name2} already exists.")
            return
        
        # does not find existing relationship
        # Ready to create and add relationship
        class1 = self.classes[class_name1]
        class2 = self.classes[class_name2]
        relationship = UMLRelationship.UMLRelationship(relationship_name, class1, class2)
        # add relationship to class objects
        class1.add_relationship(class_name2, relationship)
        class2.add_relationship(class_name1, relationship)

        # Prompt success
        print(f"Relationship between {class_name1} and {class_name2} was created")

    ######################################################################
    
    def delete_relationship(self, class_name1:str, class_name2:str):
        """Deletes a relationship between two given classes
            - class_name1 (string) - the name of the first class
            - class_name2 (string) - the name of the second class
        """
        # Class1 does not exist
        if class_name1 not in self.classes:
            print (f"{class_name1} does not exist")
            return 
        # Class2 does not exist
        if class_name2 not in self.classes:
            print (f"{class_name2} does not exist")
            return
        
        # Ensure relationship exists
        # We only need to check one class
        if not self.classes[class_name1].has_relationship(class_name2):
            print (f"Relationship between {class_name1} and {class_name2} does not exist.")
            return 

        # Remove relationship from both classes 
        self.classes[class_name1].remove_relationship(class_name2)
        self.classes[class_name2].remove_relationship(class_name1)

        print (f"Relationship between {class_name1} and {class_name2} has been deleted")

    ######################################################################
    
    def save_model(self, filename):
        """Saves the model's data to a given JSON file
            - filename (string) - the name of a JSON file to save to
        """
        # Ensure file does not exist
        if path.exists(MODEL_DIRECTORY+filename):
            
            # continuously prompt until valid answer
            answer = ""
            while answer != "yes" and answer != "no":# prompt user if they want to overwrite or not
                print (f"File {filename} already exists.")
                print ("Do you want to overwrite the file? (yes/no)")

                answer = input().lower()

            if answer == "no":
                # cancel saving 
                print ("Saving FAILED")
                return


        # object to hold JSON compatible version of the data
        raw_model = {
            "classes" : {},
            "relationships" : []
        }

        # grab class data 
        for name in self.classes:

            # raw data for the class
            raw_model["classes"][name] = {
                "name" : name,
                "attributes" : self.classes[name].attributes
            }

        # save relationship data
        # tagging is used to make sure relationships are duplicated
        tag = 0
        for name in self.classes:
            for key,relationship in self.classes[name].relationships.items():
                # if relationship wasnt already tagged/visited
                if relationship.tag == -1:
                    relationship.tag = tag
                    tag += 1

                    # create and add relationship to raw_model
                    raw_model["relationships"] += [{
                        "name"   : relationship.name,
                        "class1" : relationship.class1.name,
                        "class2" : relationship.class2.name
                    }]

        # Convert data into a JSON object
        json_data = json.dumps(raw_model, indent=4)

        # Open file and write json data
        with open(MODEL_DIRECTORY+filename, "w") as file:
            file.write(json_data)

        # Tell user that save was successful 
        print (f"Saved model to file {filename}")

    ######################################################################
    
    def load_model(self, filename):
        """Loads the UML model from a given JSON file
            - filename (string) - the name of a JSON file to load from

            NOTE: File should be a JSON file generated by save_model() to
                ensure parsing is correct 
        """

        # Ensure file exists
        if not path.exists(MODEL_DIRECTORY+filename):
            print (f"{filename} does not exist")
            return

        # Clear out previous model
        self.classes = {}

        # Holds the data loaded from json
        raw_model = {}

        # read json from file
        file = open(MODEL_DIRECTORY+filename, "r")
        raw_model = json.loads(file.read())
        file.close()

        # load classes (with attributes) into model
        for class_name in raw_model["classes"]:
            self.classes[class_name] = UMLClass.UMLClass(class_name)

            # add attributes to the class
            self.classes[class_name].attributes = raw_model["classes"][class_name]["attributes"]

        # load relationships 
        for rel in raw_model["relationships"]:
            # grab classes that are in the relationship
            c1 = self.classes[rel["class1"]]
            c2 = self.classes[rel["class2"]]
            # create relationship
            relationship = UMLRelationship.UMLRelationship(rel["name"],c1,c2)
            # add relationship to classes
            c1.add_relationship(c2.name, relationship)
            c2.add_relationship(c1.name, relationship)

        # Tell user load was successful
        print (f"Loaded model from {filename}")


    ######################################################################

    def list_classes(self):
        """
            Prints to the screen all of the classes in the current model
        """
        for class_name in self.classes:
            print (class_name)

    ######################################################################

    def list_attributes(self, class_name:str):
        """
            Prints all of the attributes for a given class
            - class_name (string) - the name of the class to print 
                attributes
        """
        # ensure class exists
        if class_name in self.classes:
            # ensure class has attributes
            if not self.classes[class_name].attributes:
                print("Class '" + class_name + "' has no attributes") 
            else:
                # loop the classes by the name
                attribute = self.classes[class_name].attributes
                for i in range(len(attribute)):
                    print(attribute[i])
        # not valid class
        else:
            print (f"{class_name} is not a class")

    ######################################################################

    def list_relationships(self, class_name:str = ""):
        """
            Prints all relationships for a given class
            
            If no class is specified, then all relationships are printed.

            - class_name (string) - the name of the class to print 
                relationships
        """
        # list relationships for a specific class
        if class_name != "":
            # ensure class exists
            if class_name in self.classes:
                print (f"Relationships for {class_name}")
                # list all relationships for the class
                if not self.classes[class_name].relationships:
                    print("Class '" + class_name + "' has no relationships")
                else:
                    for other, relationship in self.classes[class_name].relationships.items():
                        print (class_name,"---", relationship.name, "-->",relationship.get_other_class(class_name).name)

            # class_name is invalid
            else: 
                print (f"{class_name} does not exist")
        # list all relationships
        else:
            # for each class
            for class_name in self.classes:
                # for each relationship
                    for other, relationship in self.classes[class_name].relationships.items():
                        print (class_name,"---", relationship.name, "-->",relationship.get_other_class(class_name).name)

##########################################################################
