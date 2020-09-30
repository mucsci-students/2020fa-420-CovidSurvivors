# A representation of a UML Class
# Description:     
#   This file holds all data that can be associated with a UML Class
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

##########################################################################
# Imports 

from UMLField import UMLField
from UMLMethod import UMLMethod
from Visibility import Visibility

##########################################################################

class UMLClass:

    def __init__(self, name:str):
        """Represents a UML Class 
        
        Params:
        - name (string) - the name for the class
        """
        # Represents this classes name
        self.name = name
        # A list of all attributes that belong to this class
        # **This should be removed later**
        self.attributes = []
        # A list of all fields
        self.fields = []
        # A list of all methods
        self.methods = []
        # A dictionary of all relationships that this class 
        # participates in 
        # map of (other_class_name, relationship)
        self.relationships = {}

##########################################################################

    def add_field(self, visibility:str, field_name:str, _type:str):
        """Adds a field to this class

        Params:
        - visibility (string) - the visibility of a field, should be 
        'public' or 'private'
        - field_name (string) - the name for a field to add
        - _type (string) - the type of the field

        Preconditions:
        - visibility should be 'public' or 'private'
        - field_name should not already exist

        Postconditions:
        - the field will be added to this class
        """
        self.fields += [UMLField(Visibility.from_string(visibility), field_name, _type)]

##########################################################################

    def rename_field(self, old_field_name:str, new_field_name:str):
        """Renames a field in this class

        Params:
        - old_field_name (string) - the name for a field 
        - new_field_name (string) - the new name for the field

        Preconditions:
        - old_field_name should exist
        - new_field_name should not already exist

        Postconditions:
        - the field's name will be changed
        """
        # change name while keeping order
        index = self.field_index(old_field_name)
        # rename the field
        self.fields[index].rename(new_field_name)

##########################################################################

    def remove_field(self, field_name:str):
        """Removes a field from this class

        Params:
        - field_name (string) - the name for a field to remove

        Preconditions:
        - field_name should exist

        Postconditions:
        - the field will be deleted from this class
        """
        index = self.field_index(field_name)
        # remove from ordered list
        del self.fields[index]

##########################################################################

    def has_field(self, field_name:str):
        """Returns true if this class has a field matching the given name

        Params:
        - field_name (string) - the name for a field
        """
        return self.field_index(field_name) != -1

##########################################################################

    def field_index(self, field_name:str):
        """Returns the index for a given field in the list, otherwise -1
         if field is not found
        """
        # Look through each elem for the field
        for i in range(len(self.fields)):
            if self.fields[i].name == field_name:
                return i
        return -1

##########################################################################

    def add_method(self, visibility:str, method_name:str, _type:str):
        """Adds a method to this class

        Params:
        - visibility (string) - the visibility of a method, should be 
        'public' or 'private'
        - method_name (string) - the name for a method to add
        - _type (string) - the type of the method

        Preconditions:
        - visibility should be 'public' or 'private'
        - method_name should not already exist

        Postconditions:
        - the method will be added to this class
        """
        self.methods += [UMLMethod(Visibility.from_string(visibility), method_name, _type)]

##########################################################################

    def rename_method(self, old_method_name:str, new_method_name:str):
        """Renames a method in this class

        Params:
        - old_method_name (string) - the name for a method 
        - new_method_name (string) - the new name for the method

        Preconditions:
        - old_method_name should exist
        - new_method_name should not already exist

        Postconditions:
        - the method's name will be changed
        """
        # change name while keeping order
        index = self.method_index(old_method_name)
        # rename the field
        self.methods[index].rename(new_method_name)

##########################################################################

    def remove_method(self, method_name:str):
        """Removes a method from this class

        Params:
        - method_name (string) - the name for a method to remove

        Preconditions:
        - method_name should exist

        Postconditions:
        - the method will be deleted from this class
        """
        index = self.method_index(method_name)
        # remove from ordered list
        del self.methods[index]

##########################################################################

    def has_method(self, method_name:str):
        """Returns true if this class has a method matching the given name

        Params:
        - method_name (string) - the name for a method
        """
        return self.method_index(method_name) != -1

##########################################################################

    def method_index(self,method_name:str):
        """Returns the index for a given method in the list
        
        returns -1 if not present 
        """
        for i in range(len(self.methods)):
            if self.methods[i].name == method_name:
                return i
        return -1

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
