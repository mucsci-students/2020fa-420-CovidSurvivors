
##########################################

# from UMLClass import UMLClass_class

###########################################

class UMLClass:
    def _init_(self, name:str, attributes:list, relationship:list):
        self.name = name
        self.attributes = []
        self.relationships = []

#################################################      

    def add_attribute(self, attribute):
        self.attributes += [attribute]

#################################################        

    def remove_attribute(self, attribute):
        
        self.attributes.remove(attribute) 
##################################################        

    def add_relationship(self, relationship):
        
         self.relationships += [relationship]

##################################################
    def remove_relationship(self, relationship):
        self.relationship.remove(relationship)           
##################################################
