# A representation of the state of a UML Model
# Description:
#   This file keeps track of all the classes that are in the UML Model
#   It also handles saving/loading the Model to/from a JSON file
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 20 2020

##########################################################################
# Imports

import json
import sys
import os.path
from os import path
from typing import Tuple

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

    def create_class(self, name:str) -> Tuple[bool, str]:
        """Creates UML Class object and adds it to the model
            - name (string) - the name for the new class
        """
        # Ensure class does not already exist
        if name in self.classes:
            return (False, "{} already exists.".format(name))

        # Creates class object and assigns it to a key
        self.classes[name] = UMLClass(name)

        # return success
        return (True, f"Class '{name}' was created.")

    ######################################################################

    def rename_class(self, oldClassName:str, newClassName:str) -> Tuple[bool, str]:
        """Renames an existing UML Class
            oldClassName (string) - name of class to rename
            newClassName (string) - new name for the class
        """
        # Checks if the old class name exists
        if oldClassName not in self.classes:
            return (False, "{} does not exist.".format(oldClassName))

        # Checks if the new class name is already in use
        if newClassName in self.classes:
            return (False, "{} already exists.".format(newClassName))

        # Renames existing class object
        self.classes[oldClassName].name = newClassName
        # Assigns the renamed class object to a key with the new class name
        self.classes[newClassName] = self.classes.pop(oldClassName)

        # reassign this class' name in other classes relationships
        for relationship in self.classes[newClassName].relationships:
            # rename
            self.classes[relationship.other].relationships[self.classes[relationship.other].relationship_index(oldClassName)].other = newClassName

        # return success
        return (True, f"Class '{oldClassName}' was renamed to '{newClassName}'.")

    ######################################################################

    def delete_class(self, name:str) -> Tuple[bool, str]:
        """Deletes UML Class object from the model
            - name (string) - the name of the class to delete
        """
        # Ensure class exists
        if name not in self.classes:
            return (False, "{} does not exist.".format(name))

        # Delete all relationships to this class
        for rel in self.classes[name].relationships:
            self.delete_relationship(name, rel.other)

        # Deletes key-value pair for specified class
        del self.classes[name]

        # return success
        return (True, "{} has been deleted.".format(name))

    ######################################################################
    def create_field(self, class_name:str, visibility:str, field_type:str, field_name:str) -> Tuple[bool, str]:
        """Creates an attribute for a given class
            - class_name (string) - the name of the class
            - visibility (string) - the visibility of a field, should be
            'public' or 'private'
            - field_name (string) - the name of the field
            - field_type (string) - the type of the field
        """
        # Ensure class exists
        if class_name not in self.classes:
            return (False, "{} does not exist".format(class_name))

        # Ensure field does not already exist
        if self.classes[class_name].has_field(field_name):
            return (False, "field {} already exists in {}".format(field_name, class_name))

        # creates field in class
        self.classes[class_name].add_field(visibility, field_name, field_type)

        # Return success
        return (True, "field {} of type {} has been created in {}, it is a {} field"
        .format(field_name, field_type, class_name, visibility))

    ######################################################################

    def find_field(self, class_name:str, field_name:str):
        """Gives the index of a given field in a given class

            If field does not exist, then -1 is returned

            - class_name (string) - the name of the class
            - field_name (string) - the name of the field
        """
        for i in range(len(self.classes[class_name].fields)):
            # Finds the attribute
            if self.classes[class_name].fields[i].name == field_name:
                return i
        return -1

    ######################################################################
    def rename_field(self, class_name:str, old_field_name:str, new_field_name:str) -> Tuple[bool, str]:
        """Renames a field for a given class
            - class_name (string) - the name of the class
            - old_field_name (string) - the name of the field to rename
            - new_field_name (string) - the new name of the field
        """
        # checks if the class exists
        if class_name not in self.classes:
            return (False, "{} does not exist.".format(class_name))

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(old_field_name):
            return (False, "field {} does not exist in {}".format(old_field_name, class_name))

        # checks if the inputted new field name already exists in the class
        if self.classes[class_name].has_field(new_field_name):
            return (False, "field {} already exists in {}".format(new_field_name, class_name))

        # renames the field to new_field_name
        index = self.find_field(class_name, old_field_name)
        self.classes[class_name].fields[index].name = new_field_name

        # return success
        return (True, "field {} has been renamed to {}".format(old_field_name, new_field_name))

    ######################################################################
    def delete_field(self, class_name:str, field_name:str) -> Tuple[bool, str]:
        """Deletes a given field for a given class
            - class_name (string) - the name of the class
            - field_name (string) - the name for a field to
                delete
        """
        # checks if the class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(field_name):
            return (False, f"{field_name} is not a field of {class_name}")


        # deletes the field
        self.classes[class_name].remove_field(field_name)

        # gives user verification that the field was deleted
        return (True, "field {} has been deleted from {}".format(field_name, class_name))

    ###########################################################################
    def move_up_field(self, class_name:str, field_name:str):
        """Moves a field up one position in a list of fields for a given class
            - class_name (string) - the name of the class
            - field_name (string) - the name of the field being moved up
        """

        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(field_name):
            return (False, f"{field_name} does not exist in {class_name}")

        # checks if field is already at front of list
        field = self.classes[class_name].fields
        if field_name == field[0].name:
            return (False, f"{field_name} can not move up any further in {class_name}")

        for i in range(len(field)):
            #swaps target field with the field in front of it
            if field_name == field[i].name:
                mover = field[i]
                preceder = field[i-1]
                field[i-1] = mover
                field[i] = preceder
                return (True, f"{field_name} has been moved up in {class_name}")

    ######################################################################
    def move_down_field(self, class_name:str, field_name:str) -> Tuple[bool, str]:
        """Moves a field down one position in a list of fields for a given class
            - class_name (string) - the name of the class
            - field_name (string) - the name of the field being moved down
        """
        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # checks if the field exists in the class
        if not self.classes[class_name].has_field(field_name):
            return (False, f"{field_name} does not exist in {class_name}")

        # checks if field is already at back of list
        field = self.classes[class_name].fields
        if field_name == field[len(field)-1].name:
            return (False, f"{field_name} can not move down any further in {class_name}")

        for i in range(len(field)):
            #swaps target field with the field behind it
            if field_name == field[i].name:
                mover = field[i]
                succeeder = field[i+1]
                field[i+1] = mover
                field[i] = succeeder
                return (True, f"{field_name} has been moved down in {class_name}")

    ###########################################################################
    def create_relationship(self, relationship_type:str, class_name1:str, class_name2:str) -> Tuple[bool, str]:
        """Creates a relationship between two given classes
            - relationship_type (string) - the type of the relationship.
            Should be one of {inheritance, generalization, composition, aggregation}
            - class_name1 (string) - the name of the first class
            - class_name2 (string) - the name of the second class
        """
        # Ensure relationship type is valid
        rtype = RelationshipType.from_string(relationship_type)
        reverseRtype = RelationshipType.from_string("reverse " + relationship_type)
        if rtype == RelationshipType.INVALID:
            return (False, f"'{relationship_type}' is not a valid relationship type.")

        # Ensure first class exists
        if class_name1 not in self.classes:
            return (False, f"'{class_name1}' does not exist")

        # Ensure second class exists
        if class_name2 not in self.classes:
            return (False, f"'{class_name2}' does not exist")

        # Ensure relationship does not already exist
        if (self.classes[class_name1].has_relationship(class_name2) and
            self.classes[class_name2].has_relationship(class_name1)):
            return (False, f"Relationship between '{class_name1}' and '{class_name2}' already exists.")

        # does not find existing relationship
        # Ready to add relationship
        # this uses a look-before-leaping approach to weed out any bugs
        if not self.classes[class_name1].has_relationship(class_name2):
            self.classes[class_name1].add_relationship(rtype, class_name2)
        if not self.classes[class_name2].has_relationship(class_name1):
            self.classes[class_name2].add_relationship(reverseRtype, class_name1)

        # Prompt success
        return (True, f"Relationship between '{class_name1}' and '{class_name2}' was created")

    ######################################################################

    def delete_relationship(self, class_name1:str, class_name2:str) -> Tuple[bool, str]:
        """Deletes a relationship between two given classes
            - class_name1 (string) - the name of the first class
            - class_name2 (string) - the name of the second class
        """
        # Class1 does not exist
        if class_name1 not in self.classes:
            return (False, f"{class_name1} does not exist")

        # Class2 does not exist
        if class_name2 not in self.classes:
            return (False, f"{class_name2} does not exist")

        # Ensure relationship exists
        if (not self.classes[class_name1].has_relationship(class_name2) and
            not self.classes[class_name2].has_relationship(class_name1)):
            return (False, f"Relationship between {class_name1} and {class_name2} does not exist.")

        # Remove relationship from both classes
        # This has a look-before-leap approach to weed out any potential bugs
        if self.classes[class_name1].has_relationship(class_name2):
            self.classes[class_name1].remove_relationship(class_name2)
        if self.classes[class_name2].has_relationship(class_name1):
            self.classes[class_name2].remove_relationship(class_name1)

        return (True, f"Relationship between {class_name1} and {class_name2} has been deleted")

    ######################################################################

    def move_up_relationship(self, class_name1:str, class_name2:str):
        """Moves a relationship up one position in a list of relationships for tw
            - class_name1 (string) - the name of the first class
            - class_name2 (string) - the name of the second class
        """

        # ensure class 1 exists
        if class_name1 not in self.classes:
            return (False, f"{class_name1} does not exist")

        # ensure class 2 exists
        if class_name2 not in self.classes:
            return (False, f"{class_name2} does not exist")

        # ensure relationship exists
        if (not self.classes[class_name1].has_relationship(class_name2) and
            not self.classes[class_name2].has_relationship(class_name1)):
            return (False, f"Relationship between {class_name1} and {class_name2} does not exist.")

        i = self.classes[class_name1].relationship_index(class_name2)
        # check if relationship is at top of list
        if i == 0:
            return (False, f"The relationship with {class_name2} can not move up any further in {class_name1}")

        # swap with relationship in front of it
        rships = self.classes[class_name1].relationships
        mover = rships[i]
        preceder = rships[i-1]
        rships[i-1] = mover
        rships[i] = preceder
        return (True, f"The relationship with {class_name2} has been moved up in {class_name1}")

    ######################################################################

    def move_down_relationship(self, class_name1:str, class_name2:str) -> Tuple[bool, str]:
        """Moves a relationship down one position in a list of relationships
            - class_name (string) - the name of the class
            - class_name1 (string) - the name of the first class
            - class_name2 (string) - the name of the second class
        """

         # ensure class 1 exists
        if class_name1 not in self.classes:
            return (False, f"{class_name1} does not exist")

        # ensure class 2 exists
        if class_name2 not in self.classes:
            return (False, f"{class_name2} does not exist")

        # ensure relationship exists
        if (not self.classes[class_name1].has_relationship(class_name2) and
            not self.classes[class_name2].has_relationship(class_name1)):
            return (False, f"Relationship between {class_name1} and {class_name2} does not exist.")

        i = self.classes[class_name1].relationship_index(class_name2)
        rships = self.classes[class_name1].relationships
        # checks if relationship is already at back of list
        if i == len(rships)-1:
            return (False, f"The relationship with {class_name2} can not move down any further in {class_name1}")

        # swaps target relationship with the relationship behind it
        mover = rships[i]
        succeeder = rships[i+1]
        rships[i+1] = mover
        rships[i] = succeeder

        return (True, f"The relationship with {class_name2} has been moved down in {class_name1}")

    ######################################################################

    def save_model(self, filename, directory=MODEL_DIRECTORY) -> Tuple[bool, str]:
        """Saves the model's data to a given JSON file
            - filename (string) - the name of a JSON file to save to
        """

        # object to hold JSON compatible version of the data
        raw_model = self.get_data()

        # Convert data into a JSON object
        json_data = json.dumps(raw_model, indent=4)

        # Open file and write json data
        with open(directory+filename, "w") as file:
            file.write(json_data)

        # Tell user that save was successful
        return (True, f"Saved model to file {filename}")

    def get_data(self):
        raw_model = {}
        for name in self.classes:
            # raw data for the class
            raw_model[name] = self.classes[name].get_raw_data()
        return raw_model

    ######################################################################

    def load_model(self, filename:str, directory=MODEL_DIRECTORY) -> Tuple[bool, str]:
        """Loads the UML model from a given JSON file
            - filename (string) - the name of a JSON file to load from
            - path (str) - the path for the data folder

            NOTE: File should be a JSON file generated by save_model() to
                ensure parsing is correct
        """

        # Ensure file exists
        if not path.exists(directory+filename):
            return (False, f"{directory+filename} does not exist")

        # Holds the data loaded from json
        raw_model = {}

        # read json from file
        file = open(MODEL_DIRECTORY+filename, "r")
        try:
            raw_model = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            return (False, "File cannot be parsed. Invalid JSON")
        file.close()

        status, msg = self.set_data(raw_model)

        # parse failed
        if not status:
            return status, msg

        # Tell user load was successful
        return (True, f"Loaded model from {filename}")

    ######################################################################

    def set_data(self, raw_model:dict) -> Tuple[bool, str]:
        # grab classes
        classes = {}
        for class_name in raw_model:
            # build class
            newclass = None
            try:
                newclass = UMLClass.from_raw_data(raw_model[class_name])
            except TypeError:
                return (False, "File cannot be parsed")
            except KeyError:
                return (False, "File cannot be parsed")
            # ensure class was created successfully 
            if newclass == None:
                return (False, "File cannot be parsed")
            # add class
            classes[newclass.name] = newclass

        # parse was successful
        # reassign this model to the parsed class data 
        self.classes = classes
        return (True, "Model data set successfully")

    ######################################################################

    def list_class(self, class_name) -> Tuple[bool, str]:
        """
            Prints all information about a given class
        """
        # Ensure class exists
        if class_name not in self.classes:
            return (False, f"'{class_name}' is not a valid class")

        outputs = [f"Class: {class_name}"]

        outputs.append("=== Fields ======================")

        # Print fields
        for field in self.classes[class_name].fields:
            outputs.append(f"{Visibility.to_string(field.visibility)} {field.name}: {field.type}")

        outputs.append("=== Methods =====================")

        # Print methods
        for method in self.classes[class_name].methods:
            method_str = f"{Visibility.to_string(method.visibility)} {method.name}("
            
            # print parameters
            # add first parameter
            if len(method.parameters) >= 1:
                method_str = "".join([method_str, f"{method.parameters[0].type} {method.parameters[0].name}"])
            for i in range(1, len(method.parameters)):
                method_str = ", ".join([method_str, f"{method.parameters[i].type} {method.parameters[i].name}"])
            
            # add end of method line
            method_str = "".join([method_str, f"): {method.type}"])
            # add to output
            outputs.append(method_str)

        outputs.append("=== Relationships ===============")

        # Print relationships
        for relationship in self.classes[class_name].relationships:
            outputs.append(f"{class_name} {RelationshipType.to_arrow(relationship.type)} {relationship.other}")

        outputs.append("=================================")

        return (True, "\n".join(outputs))

    ######################################################################

    def list_classes(self) -> Tuple[bool, str]:
        """
            Prints to the screen all of the classes in the current model
        """
        outputs = ["Listing all classes in the model"]
        for class_name in self.classes:
            outputs.append(class_name)

        # ensure there were classes
        if len(outputs) == 1:
            return (True, f"No classes in the model")

        return (True, "\n".join(outputs))

    ######################################################################

    def list_fields(self, class_name:str) -> Tuple[bool, str]:
        """
            Prints all of the fields for a given class
            - class_name (string) - the name of the class to print
                fields
        """
        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} is not a class")

        # ensure class has fields
        if not self.classes[class_name].fields:
            return (True, "Class '" + class_name + "' has no fields")

        # loop the classes by the name
        outputs = [f"Fields of {class_name}"]
        field = self.classes[class_name].fields
        for i in range(len(field)):
            outputs.append(f"{field[i].visibility.name} {field[i].type} {field[i].name}")

        return (True, "\n".join(outputs))

    ######################################################################

    def list_relationships(self, class_name:str = "") -> Tuple[bool, str]:
        """
            Prints all relationships for a given class

            If no class is specified, then all relationships are printed.

            - class_name (string) - the name of the class to print
                relationships
        """
        # list relationships for a specific class
        if class_name != "":

            # ensure class exists
            if class_name not in self.classes:
                return (False, f"{class_name} does not exist")

            # ensure class has relationships
            if not self.classes[class_name].relationships:
                return (True, "Class '" + class_name + "' has no relationships")

            # list all relationships for the class
            outputs = [f"Relationships for {class_name}"]
            for relationship in self.classes[class_name].relationships:
                outputs.append(f"{class_name} {RelationshipType.to_arrow(relationship.type)} {relationship.other}")
            return (True, "\n".join(outputs))

        # list all relationships
        else:
            outputs = ["Listing all relationships"]
            # for each class
            for class_name in self.classes:
                # for each relationship
                for relationship in self.classes[class_name].relationships:
                    outputs.append(f"{class_name} {RelationshipType.to_arrow(relationship.type)} {relationship.other}")

            # ensure there were relationships
            if len(outputs) == 1:
                return (True, "No relationships exist for the current model")

            return (True, "\n".join(outputs))

##########################################################################

    def create_method(self, class_name:str, visibility:str, method_type:str, method_name:str) -> Tuple[bool, str]:
        """Creates a method for a given class
            - class_name (string) - the name of the class
            - visibility (string) - the visibility of a method, should be 'public', 'private', or 'protected'
            - method_name (string) - the name of the method
            - method_type (string) - the type of the method
        """
         # checks if the the class exists
        if class_name not in self.classes:
            return (False, "{} does not exist".format(class_name))

        # checks if the class does not have an method with the same name inputted
        if self.classes[class_name].has_method(method_name):
            return (False, "method {} already exists in {}".format(method_name, class_name))

        # creates method in class
        self.classes[class_name].add_method(visibility, method_name, method_type)
        return (True, "method {} of type {} has been created in {}, it is a {} method"
            .format(method_name, method_type, class_name, visibility))

    ######################################################################################

    def rename_method(self, class_name:str, old_method_name:str, new_method_name:str) -> Tuple[bool, str]:
        """
            - Renames a method for a given class
            - class_name (string) - the name of the class
            - old_method_name (string) - the name of the method to rename
             - new_method_name (string) - the new name of the method
        """
        # checks if the class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(old_method_name):
            return (False, "method {} does not exist in {}".format(old_method_name, class_name))

        # checks if the inputted new method name already exists in the class
        if self.classes[class_name].has_method(new_method_name):
            return (False, "method '{}' already exists in '{}'".format(new_method_name, class_name))

        # renames the old_method_name to new_method_name
        self.classes[class_name].rename_method(old_method_name, new_method_name)
        return (True, "method '{}' has been renamed to '{}'".format(old_method_name, new_method_name))

    ############################################################

    def delete_method(self, class_name:str, method_name:str) -> Tuple[bool, str]:
        """Deletes a given method for a given class
            - class_name (string) - the name of the class
            - method_name (string) - the name for a method to
                delete
        """
        # checks if the class exists
        if class_name not in self.classes:
            return (False, f"'{class_name}' does not exist")

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(method_name):
            return (False, f"'{method_name}' does not exist in '{class_name}'")

        # deletes the method
        self.classes[class_name].remove_method(method_name)

        # gives user verification that the method was deleted
        return (True, "method '{}' has been deleted from '{}'".format(method_name, class_name))

    ######################################################################

    def move_up_method(self, class_name:str, method_name:str) -> Tuple[bool, str]:
        """Moves a method up one position in a list of methods for a given class
            - class_name (string) - the name of the class
            - method_name (string) - the name of the method being moved up
        """

        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(method_name):
            return (False, f"{method_name} does not exist in {class_name}")

        # checks if method is already at front of list
        method = self.classes[class_name].methods
        if method_name == method[0].name:
            return (False, f"{method_name} can not move up any further in {class_name}")

        for i in range(len(method)):
            #swaps target method with the method in front of it
            if method_name == method[i].name:
                mover = method[i]
                preceder = method[i-1]
                method[i-1] = mover
                method[i] = preceder

                return (True, f"{method_name} has been moved up in {class_name}")

    ######################################################################

    def move_down_method(self, class_name:str, method_name:str) -> Tuple[bool, str]:
        """Moves a method down one position in a list of methods for a given class
            - class_name (string) - the name of the class
            - method_name (string) - the name of the method being moved down
        """
        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # checks if the method exists in the class
        if not self.classes[class_name].has_method(method_name):
            return (False, f"{method_name} does not exist in {class_name}")

        # checks if method is already at back of list
        method = self.classes[class_name].methods
        if method_name == method[len(method)-1].name:
            return (False, f"{method_name} can not move down any further in {class_name}")

        for i in range(len(method)):
            #swaps target method with the method behind it
            if method_name == method[i].name:
                mover = method[i]
                succeeder = method[i+1]
                method[i+1] = mover
                method[i] = succeeder

                return (True, f"{method_name} has been moved down in {class_name}")

    ######################################################################

    def list_methods(self, class_name:str):
        """
            Prints all of the methods for a given class

            - class_name (string) - the name of the class to print
            methods
        """
        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # ensure class has methods
        if not self.classes[class_name].methods:
            return (True, f"{class_name} has no methods")

        # loop the classes by the name
        outputs = [f"Methods for {class_name}"]
        for method in self.classes[class_name].methods:
            outputs.append(f"{method.visibility.name} {method.name}() : {method.type}")

        return (True, "\n".join(outputs))

    ######################################################################

    def set_class_position(self, class_name:str, x:int, y:int, zindex:int):
        """
            Sets the x and y position of a given class based on the position
            of that class on the dashboard of the GUI

            - class_name (string) - the name of the class to set the position of

            - x (float) - the horizontal (CSS left property) position of the class card

            - y (float) - the vertical (CSS top property) position of the class card
        """

        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # set the x position
        (self.classes[class_name]).x = x
        # set the y position
        (self.classes[class_name]).y = y
        # set the z-index
        (self.classes[class_name]).zindex = zindex

        # gives user verification that the positions have been set
        return (True, f"The position of '{class_name}' has been set to ('{x}', '{y}')")

    ######################################################################

    def create_parameter(self, class_name:str, method_name:str, parameter_type:str, parameter_name:str)-> Tuple[bool, str]:
        """Creates parameters for a given class within method
            - class_name (string) - the name of the class
            - method_name (string) - the name of the method
            - parameter_type (string) - the type of the parameter
            - parameter_name (string) - the name of the parameter
        """
        #checks if the the class exists
        if class_name not in self.classes:
            return (False, "{} does not exist".format(class_name))

        #ensure the method name exist
        if not self.classes[class_name].has_method(method_name):
            return (False, "method {} does not exist in {}".format(method_name, class_name))

        # ensure the parameter do not exist
        if self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].has_parameter(parameter_name):
            return (False, " {} already exists in {}".format(parameter_name, method_name))

        # creates parameter in class
        self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].create_parameter(parameter_type, parameter_name)
        return (True, "parameter {} of type {} has been created in {}"
            .format(parameter_name, parameter_type, method_name))
    ##########################################################################

    def list_parameters(self, class_name:str, method_name:str):
        """
            Prints all of the parameters for a given method of a given class

            - class_name (string) - the name of the class
            - method_name (string) - the name of the method
        """
        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # ensure class has methods
        if not self.classes[class_name].has_method(method_name):
            return (False, f"{class_name} does not have method, {method_name}")

        # loop the classes by the name
        outputs = [f"Parameters for {method_name}"]
        for parameter in self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].parameters:
            outputs.append(f"({parameter.type}):{parameter.name}")

        return (True, "\n".join(outputs))

    ##########################################################################
    
    def rename_parameter(self, class_name:str, method_name:str, old_parameter_name:str, new_parameter_name:str)-> Tuple[bool, str]:
        """Rename parameters in a class for a given method
            - class_name(string) - the name of the class
            - method_name (string) - the name of the method
            - old_parameter_name (string) - the name of the parameter
            - new_parameter_name (string) - the name of the parameter
        """

        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        
        # ensure class has methods
        if not self.classes[class_name].has_method(method_name):
            return (False, f"{class_name} does not have method, {method_name}")   
            
        # ensure the parameter exist
        if not self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].has_parameter(old_parameter_name):
            return (False, " {} does not exists in {}".format(old_parameter_name, method_name)) 

        # checks if the inputted new method name already exists in the class
        if self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].has_parameter(new_parameter_name):
            return (False, " {} already exists in {}".format(new_parameter_name, method_name))   

        # renames the old_parameter_name to new_parameter_name
        self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].rename_parameter(old_parameter_name, new_parameter_name)
        return (True, "parameter '{}' has been renamed to '{}'".format(old_parameter_name, new_parameter_name))
        
    ##########################################################################
    
    def delete_parameter(self, class_name:str, method_name:str, parameter_name:str)-> Tuple[bool, str]:
        """Delete parameters in a class for a given method
            - class_name(string) - the name of the class
            - method_name (string) - the name of the method
            - parameter_name (string) - the name of the parameter to delete
        """

        # ensure class exists
        if class_name not in self.classes:
            return (False, f"{class_name} does not exist")

        # ensure class has the method_name
        if not self.classes[class_name].has_method(method_name):
            return (False, f"{class_name} does not have method, {method_name}")   
            
        # ensure the parameter exist
        if not self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].has_parameter(parameter_name):
            return (False, " {} does not exists in {}".format(parameter_name, method_name)) 

        # delete the parameter
        self.classes[class_name].methods[self.classes[class_name].method_index(method_name)].delete_parameter(parameter_name)
        # gives user verification that the parameter was deleted
        return (True, "parameter '{}' has been removed from '{}'".format(parameter_name, method_name))
        
    ##########################################################################
