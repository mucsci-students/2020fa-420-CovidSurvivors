

##########################################################################

from UMLClass import UMLClass

##########################################################################

# Represents the relationship between 2 UML Classes 
class UMLRelationship:

    ######################################################################

    # Constructs a UML Relationship object with the 
    # given name and given UML classes 
    # @precondition - class1 and class2 are UMLClass objects that have
    #   been initialized 
    def __init__(self, name:str, class1:UMLClass, class2:UMLClass):
        self.name = name
        self.class1 = class1
        self.class2 = class2

    ######################################################################

##########################################################################