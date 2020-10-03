# A representation of a Method for a UML
# Description:     
#   This file encapsulates the idea of a method of a class
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 27 2020

##########################################################################
# Imports

from .Visibility import Visibility

##########################################################################

class UMLMethod:

    def __init__(self, visibility:Visibility, name:str, _type:str):
        """Represents a method for a UML Class
        
        Params: 
        - visibility (Visibility) - the visibility of the method,
         either Public or Private
        - name (str) - the name of the method
        - _type (str) - the return type of the method
        """
        self.visibility = visibility
        self.name = name
        self.type = _type

    ######################################################################

    def rename(self, new_name:str):
        """Replaces the method's name with a new_name
        """
        self.name = new_name

##########################################################################

    def get_raw_data(self):
        """Returns a JSON convertible form of the data"""
        return {
                "visibility" : Visibility.to_string(self.visibility),
                "name" : self.name, 
                "type" : self.type
            }

##########################################################################

    @staticmethod
    def from_raw_data(data):
        """Constructs a UMLMethod object from a set of data
        
        Precondition:
        - The data should have been generated by a call to get_raw_data()
        """
        return UMLMethod(Visibility.from_string(data["visibility"]), data["name"], data["type"])
            
##########################################################################