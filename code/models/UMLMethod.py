# A representation of a Method for a UML
# Description:
#   This file encapsulates the idea of a method of a class
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 27 2020

##########################################################################
# Imports

from models.Variable import Variable
from .Visibility import Visibility
from models.UMLParameter import UMLParameter

##########################################################################

class UMLMethod(Variable):

    def __init__(self, visibility:Visibility, name:str, _type:str, isstatic:bool=False):
        """Represents a method for a UML Class

        Params:
        - visibility (Visibility) - the visibility of the method,
         either Public or Private
        - name (str) - the name of the method
        - _type (str) - the return type of the method
        - isstatic (bool) - whether the method is static or not
        """
        self.visibility = visibility
        # Assign name and type in the parent
        super().__init__(_type, name)
        # Keeps track of whether this is a static method or not
        self.is_static = isstatic
        # keeps track of all the parameters for this class
        self.parameters = []

##########################################################################

    def create_parameter(self, parameter_type:str, parameter_name:str):
        """Add new pararameters (name , type)
        Params:
        - parameter_type (string) - the type of the parameter
        - parameter_name (string) - the name of the parameter

        Preconditions:
        - parameter_name should not already exist

        Postconditions:
        - the parameter within method will be added to this class

        """

        self.parameters.append(UMLParameter(parameter_type, parameter_name))

##########################################################################
    def rename_parameter(self, old_parameter_name:str, new_parameter_name:str):
        """Edit an existed pararameter (old_parameter_name , new_parameter_type)
        Params:
        - old_parameter_name (string) - the name of the parameter
        - old_parameter_type (string) - the type of the parameter

        Preconditions:
        - new_parameter_name should not already exist

        Postconditions:
        - the old_parameter_name within method will be edited from this class

        """

        self.parameters[self.parameter_index(old_parameter_name)].rename(new_parameter_name)

##########################################################################
    def delete_parameter(self, parameter_name:str):
        """Removes a parameter within this method class

        Params:
        - method_name (string) - the name for a parameter to remove wthin this method class

        Preconditions:
        - parameter_name should exist

        Postconditions:
        - the parameter will be deleted
        """

        self.parameters.pop(self.parameter_index(parameter_name))

##########################################################################

    def parameter_index(self, parameter_name:str):
        """Returns the index for a given parameter in the list

        returns -1 if not present
        """
        for i in range(len(self.parameters)):
            if self.parameters[i].name == parameter_name:
                return i
        return -1

##########################################################################

    def has_parameter(self, parameter_name:str):
        """Returns true if this class has a parameter matching the given name

        Params:
        - parameter_name (string) - the name for a parameter
        """
        return self.parameter_index(parameter_name) != -1

##########################################################################

    def get_raw_data(self):
        """Returns a JSON convertible form of the data"""
        return {
                "visibility" : Visibility.to_string(self.visibility),
                "name" : self.name,
                "type" : self.type,
                "parameters" : [param.get_raw_data() for param in self.parameters]
            }

##########################################################################

    @staticmethod
    def from_raw_data(data):
        """Constructs a UMLMethod object from a set of data

        Precondition:
        - The data should have been generated by a call to get_raw_data()
        """
        method = UMLMethod(Visibility.from_string(data["visibility"]), data["name"], data["type"])
        # add parameters
        if "parameters" in data:
            method.parameters = [UMLParameter.from_raw_data(param) for param in data["parameters"]]
        return method

##########################################################################
