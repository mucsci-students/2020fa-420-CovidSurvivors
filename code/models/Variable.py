# A representation of a variable for a UML model
# Description:     
#   This is an abstraction of different types of variables 
#   like fields, methods, or parameters 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 21 2020

##########################################################################
# Imports


##########################################################################

class Variable:

    def __init__(self, type:str, name:str):
        self.type = type
        self.name = name
        
    def set_type(self, new_type:str):
        """Replaces the variable's type with a new_type
        """
        self.type = new_type

    def rename(self, new_name:str):
        """Replaces the variable's name with a new_name
        """
        self.name = new_name

##########################################################################
