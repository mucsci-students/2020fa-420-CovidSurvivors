# A representation of a Field for a UML
# Description:     
#   This file encapsulates the idea of a field of a class
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 27 2020

##########################################################################
# Imports

from Visibility import Visibility

##########################################################################

class UMLField:

    def __init__(self, visibility:Visibility, name:str, _type:str):
        """Represents a field for a UML Class
        
        Params: 
        - visibility (Visibility) - the visibility of the field,
         either Public or Private
        - name (str) - the name of the field
        - _type (str) - the type of the field
        """
        self.visibility = visibility
        self.name = name
        self.type = _type

    ######################################################################

    def rename(self, new_name:str):
        """Replaces the field's name with a new_name
        """
        self.name = new_name

##########################################################################
