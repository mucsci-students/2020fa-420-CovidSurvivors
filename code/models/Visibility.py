# Simple Enum for a visibility 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 27 2020

##########################################################################
# Imports

from enum import Enum

##########################################################################

class Visibility(Enum):
    PUBLIC = 1
    PRIVATE = 2
    PROTECTED = 3
    INVALID = 4
    
##########################################################################

    @staticmethod
    def from_string(vis:str):
        """Converts a string to a Visibility type

        if 'public' -> Visibility.PUBLIC

        if 'private' -> Visibility.PRIVATE

        if 'protected' -> Visibility.PROTECTED

        otherwise Visibility.INVALID is returned
        """
        if vis == "public":
            return Visibility.PUBLIC
        elif vis == "private":
            return Visibility.PRIVATE
        elif vis == "protected":
            return Visibility.PROTECTED    
        return Visibility.INVALID

##########################################################################

    @staticmethod
    def to_string(vis):
        """Converts a visibility type enum to a string representation"""
        if vis == Visibility.PUBLIC:
            return "public"
        elif vis == Visibility.PRIVATE:
            return "private"
        elif vis == Visibility.PROTECTED:
            return "protected"      
        return "invalid"

##########################################################################
