# A representation of the state of a UML Model
# Description:     
#   This file keeps track of all the classes that are in the UML Model
#   It also handles saving/loading the Model to/from a JSON file 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

##########################################################################
# Imports

import json
import sys
import os.path
from os import path

# Relative imports
from .UMLClass import UMLClass
from .UMLRelationship import UMLRelationship
from .Visibility import Visibility
from .RelationshipType import RelationshipType


##########################################################################
# Constants 

# The directory where models are saved
MODEL_DIRECTORY = os.path.join(os.getcwd(), "data/")

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
            self.classes[name] = UMLClass(name)

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
            # Delete all relationships to this class
            for rel in self.classes[name].relationships:
                self.delete_relationship(name, rel.other)
            # Deletes key-value pair for specified class
            del self.classes[name]
            print("{} has been deleted.".format(name))
        else:
            print("{} does not exist.".format(name))

    ######################################################################
    def create_field(self, class_name:str, visibility:str, field_type:str, field_name:str):
        """Creates an attribute for a given class
            - class_name (string) - the name of the class
            - visibility (string) - the visibility of a field, should be 
            'public' or 'private'
            - field_name (string) - the name of the field
            - field_type (string) - the type of the field
        """
        # checks if the the class exists
        if class_name in self.classes:
            # checks if the class does not have an field with the same name inputted
            if not self.classes[class_name].has_field(field_name):
                # creates field in class
                self.classes[class_name].add_field(visibility, field_name, field_type)
                print("field {} of type {} has been created in {}, it is a {} field"
                .format(field_name, field_type, class_name, visibility))
            else:
                print("field {} already exists in {}".format(field_name, class_name))   
        else:
            print("{} does not exist".format(class_name))

    ######################################################################
    
    def find_field(self, class_name:str, field_name:str):
        """Gives the index of a given field in a given class

            If field does not exist, then -1 is returned 

            - class_name (string) - the name of the class
            - field_name (string) - the name of the field 
        """
        for i in range(len(self.classes[class_name].fields)):
            # Finds the attribute 
            if self.classes[class_name].fields[i] == field_name:
                return i
        return -1     

    ######################################################################
    def rename_field(self, class_name:str, old_field_name:str, new_field_name:str):
        """Renames a field for a given class
            - class_name (string) - the name of the class
            - old_field_name (string) - the name of the field to rename
            - new_field_name (string) - the new name of the field
        """
        # checks if the class exists
        if class_name not in self.classes:
            print("{} does not exist.".format(class_name))
            return

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(old_field_name):
            print("field {} does not exist in {}".format(old_field_name, class_name))
            return
        
        # checks if the inputted new field name already exists in the class
        if self.classes[class_name].has_field(new_field_name):  
            print("field {} already exists in {}".format(new_field_name, class_name))
            return
                
        # renames the field to new_field_name
        index = self.find_field(class_name, old_field_name)
        self.classes[class_name].fields[index].name = new_field_name
        print("field {} has been renamed to => {}".format(old_field_name, new_field_name))

    ######################################################################
    def delete_field(self, class_name:str, field_name:str):
        """Deletes a given field for a given class
            - class_name (string) - the name of the class
            - field_name (string) - the name for a field to 
                delete
        """
        # checks if the class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return 

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(field_name):
            print(f"{field_name} is not a field of {class_name}")

        
        # deletes the field
        self.classes[class_name].remove_field(field_name)

        # gives user verification that the field was deleted
        print("field {} has been deleted from {}".format(field_name, class_name))
    ###########################################################################
    def move_up_field(self, class_name:str, field_name:str):
        """Moves a field up one position in a list of fields for a given class
            - class_name (string) - the name of the class
            - field_name (string) - the name of the field being moved up
        """
        
        # ensure class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(field_name):
            print(f"{field_name} does not exist in {class_name}")
            return

        else:
            # checks if field is already at front of list
            field = self.classes[class_name].fields
            if field_name == field[0].name:
                print(f"{field_name} can not move up any further in {class_name}")
                return
            else:
                for i in range(len(field)):
                    #swaps target field with the field in front of it
                    if field_name == field[i].name:
                        mover = field[i]
                        preceder = field[i-1]
                        field[i-1] = mover
                        field[i] = preceder
                        print(f"{field_name} has been moved up in {class_name}")
                        return

    ######################################################################
    def move_down_field(self, class_name:str, field_name:str):
        """Moves a field down one position in a list of fields for a given class
            - class_name (string) - the name of the class
            - field_name (string) - the name of the field being moved down
        """
        # ensure class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(field_name):
            print(f"{field_name} does not exist in {class_name}")
            return

        else:
            # checks if field is already at back of list
            field = self.classes[class_name].fields
            if field_name == field[len(field)-1].name:
                print(f"{field_name} can not move down any further in {class_name}")
                return
            else:
                for i in range(len(field)):
                    #swaps target field with the field behind it
                    if field_name == field[i].name:
                        mover = field[i]
                        succeeder = field[i+1]
                        field[i+1] = mover
                        field[i] = succeeder
                        print(f"{field_name} has been moved down in {class_name}")
                        return

    ###########################################################################
    def create_relationship(self, relationship_type:str, class_name1:str, class_name2:str):
        """Creates a relationship between two given classes
            - relationship_type (string) - the type of the relationship.
            Should be one of {inheritance, generalization, composition, aggregation}
            - class_name1 (string) - the name of the first class
            - class_name2 (string) - the name of the second class
        """
        # Ensure relationship type is valid 
        rtype = RelationshipType.from_string(relationship_type)
        if rtype == RelationshipType.INVALID:
            print (f"'{relationship_type}' is not a valid relationship type.")
            return 
        # Ensure first class exists
        if class_name1 not in self.classes:
            print (f"'{class_name1}' does not exist")
            return
        # Ensure second class exists
        if class_name2 not in self.classes:
            print (f"'{class_name2}' does not exist")
            return 

        # Ensure relationship does not already exist
        if self.classes[class_name1].has_relationship(class_name2):
            print(f"Relationship between '{class_name1}' and '{class_name2}' already exists.")
            return
        if self.classes[class_name2].has_relationship(class_name1):
            print(f"Relationship between '{class_name1}' and '{class_name2}' already exists.")
            return
        
        # does not find existing relationship
        # Ready to add relationship
        self.classes[class_name1].add_relationship(rtype, class_name2)
        self.classes[class_name2].add_relationship(rtype, class_name1)

        # Prompt success
        print(f"Relationship between '{class_name1}' and '{class_name2}' was created")

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
        # ** Commented out because it stalls the server **
        # if path.exists(MODEL_DIRECTORY+filename):
            
        #     # continuously prompt until valid answer
        #     answer = ""
        #     while answer != "yes" and answer != "no":# prompt user if they want to overwrite or not
        #         print (f"File {filename} already exists.")
        #         print ("Do you want to overwrite the file? (yes/no)")

        #         answer = input().lower()

        #     if answer == "no":
        #         # cancel saving 
        #         print ("Saving FAILED")
        #         return


        # object to hold JSON compatible version of the data
        raw_model = {}

        # grab class data 
        for name in self.classes:
            # raw data for the class
            raw_model[name] = self.classes[name].get_raw_data()

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

        # Holds the data loaded from json
        raw_model = {}

        # read json from file
        file = open(MODEL_DIRECTORY+filename, "r")
        raw_model = json.loads(file.read())
        file.close()

        # Clear out previous model
        self.classes = {class_name : UMLClass.from_raw_data(raw_model[class_name]) for class_name in raw_model}

        # Tell user load was successful
        print (f"Loaded model from {filename}")


    ######################################################################

    def list_class(self, class_name):
        """
            Prints all information about a given class
        """
        # Ensure class exists
        if class_name not in self.classes:
            print (f"'{class_name}' is not a valid class")
        
        print (f"Class: {class_name}")

        print ("=== Fields ======================")

        # Print fields 
        for field in self.classes[class_name].fields:
            print (f"{Visibility.to_string(field.visibility)} {field.name}: {field.type}")

        print ("=== Methods =====================")

        # Print methods 
        for method in self.classes[class_name].methods:
            print (f"{Visibility.to_string(method.visibility)} {method.name}(): {method.type}")

        print ("=== Relationships ===============")

        # Print relationships 
        for relationship in self.classes[class_name].relationships:
            print (RelationshipType.to_string(relationship.type), relationship.other)

        print ("=================================")

    ######################################################################

    def list_classes(self):
        """
            Prints to the screen all of the classes in the current model
        """
        for class_name in self.classes:
            print (class_name)

    ######################################################################

    def list_fields(self, class_name:str):
        """
            Prints all of the fields for a given class
            - class_name (string) - the name of the class to print 
                fields
        """
        # ensure class exists
        if class_name in self.classes:
            # ensure class has fields
            if not self.classes[class_name].fields:
                print("Class '" + class_name + "' has no fields") 
            else:
                # loop the classes by the name
                field = self.classes[class_name].fields
                for i in range(len(field)):
                    print("{} '{}'".format(field[i].type, field[i].name))
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
                    for relationship in self.classes[class_name].relationships:
                        print (class_name,"---", relationship.type, "-->",relationship.other)

            # class_name is invalid
            else: 
                print (f"{class_name} does not exist")
        # list all relationships
        else:
            # for each class
            for class_name in self.classes:
                # for each relationship
                    for relationship in self.classes[class_name].relationships:
                        print (class_name,"---", relationship.type, "-->",relationship.other)

##########################################################################

    def create_method(self, class_name:str, visibility:str, method_type:str, method_name:str):
        """Creates a method for a given class
            - class_name (string) - the name of the class
            - visibility (string) - the visibility of a method, should be 'public' or 'private'
            - method_name (string) - the name of the method
            - method_type (string) - the type of the method
        """
         # checks if the the class exists
        if class_name in self.classes:
            # checks if the class does not have an method with the same name inputted
            if not self.classes[class_name].has_method(method_name):
                # creates method in class
                self.classes[class_name].add_method(visibility, method_name, method_type)
                print("method {} of type {} has been created in {}, it is a {} method"
                .format(method_name, method_type, class_name, visibility))
            else:
                print("method {} already exists in {}".format(method_name, class_name))     
        else:
            print("{} does not exist".format(class_name))
    
    ######################################################################################  
    
    def rename_method(self, class_name:str, old_method_name:str, new_method_name:str):
        """
            - Renames a method for a given class
            - class_name (string) - the name of the class
            - old_method_name (string) - the name of the method to rename
             - new_method_name (string) - the new name of the method
        """
        # checks if the class exists
        if class_name not in self.classes:
            print (f"{class_name} does not exist")
            return

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(old_method_name):
            print("method => {} does not exist in {}".format(old_method_name, class_name))
            return

        # checks if the inputted new method name already exists in the class
        if self.classes[class_name].has_method(new_method_name):  
            print("method => {} already exists in {}".format(new_method_name, class_name))
            return
                
        # renames the old_method_name to new_method_name
        self.classes[class_name].rename_method(old_method_name, new_method_name)
        print("method => {} has been renamed to => {}".format(old_method_name, new_method_name))
    
    ############################################################
    
    def delete_method(self, class_name:str, method_name:str):
        """Deletes a given method for a given class
            - class_name (string) - the name of the class
            - method_name (string) - the name for a method to 
                delete
        """
        # checks if the class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return 

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(method_name):
            print(f"{method_name} does not exist in {class_name}")
            return

        # deletes the method
        self.classes[class_name].remove_method(method_name)

        # gives user verification that the method was deleted
        print("method => {} has been deleted from => {}".format(method_name, class_name))

    ######################################################################
   
    def move_up_method(self, class_name:str, method_name:str):
        """Moves a method up one position in a list of methods for a given class
            - class_name (string) - the name of the class
            - method_name (string) - the name of the method being moved up
        """
        
        # ensure class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(method_name):
            print(f"{method_name} does not exist in {class_name}")
            return

        else:
            # checks if method is already at front of list
            method = self.classes[class_name].methods
            if method_name == method[0].name:
                print(f"{method_name} can not move up any further in {class_name}")
                return
            else:
                for i in range(len(method)):
                    #swaps target method with the method in front of it
                    if method_name == method[i].name:
                        mover = method[i]
                        preceder = method[i-1]
                        method[i-1] = mover
                        method[i] = preceder
                        print(f"{method_name} has been moved up in {class_name}")
                        return

    ######################################################################

    #wip
    def move_down_method(self, class_name:str, method_name:str):
        """Moves a method down one position in a list of methods for a given class
            - class_name (string) - the name of the class
            - method_name (string) - the name of the method being moved down
        """
        # ensure class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(method_name):
            print(f"{method_name} does not exist in {class_name}")
            return

        else:
            # checks if method is already at back of list
            method = self.classes[class_name].methods
            if method_name == method[len(method)-1].name:
                print(f"{method_name} can not move down any further in {class_name}")
                return
            else:
                for i in range(len(method)):
                    #swaps target method with the method behind it
                    if method_name == method[i].name:
                        mover = method[i]
                        succeeder = method[i+1]
                        method[i+1] = mover
                        method[i] = succeeder
                        print(f"{method_name} has been moved down in {class_name}")
                        return
        





    ######################################################################
    
    def list_methods(self, class_name:str):
        """
            Prints all of the methods for a given class
            
            - class_name (string) - the name of the class to print 
            methods
        """
        # ensure class exists
        if class_name not in self.classes:
            print(f"{class_name} does not exist")
            return
        
        # ensure class has methods
        if not self.classes[class_name].methods:
            print (f"{class_name} has no methods") 
            return
        
        # loop the classes by the name
        for method in self.classes[class_name].methods:
            print (class_name,"---", method.type, "-->", method.name)
            
    ######################################################################

    