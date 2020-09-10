# A representation of the state of a UML Model
# Description:     
#   This file keeps track of all the classes that are in the UML Model
#   It also handles saving/loading the Model to/from a JSON file 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 8 2020

##########################################################################
# Imports

import UMLClass
import UMLRelationship
import json

##########################################################################
# Constants 

# the directory where models are saved
MODEL_DIRECTORY = "models/"

##########################################################################


# Representation of a UML Model
class UMLModel:

    ######################################################################
    
    # Constructs an empty UML Model
    def __init__(self):
        
        # Dictionary mapping class names to their class object
        self.classes = {}

        # ** Testing data **

        class1 = UMLClass.UMLClass("class1")
        class2 = UMLClass.UMLClass("class2")
        class3 = UMLClass.UMLClass("class3")
        class4 = UMLClass.UMLClass("class4")
        self.classes[class1.name] = class1
        self.classes[class2.name] = class2
        self.classes[class3.name] = class3
        self.classes[class4.name] = class4

        rel1 = UMLRelationship.UMLRelationship("temp", class2, class1)
        class1.add_relationship(rel1)
        class2.add_relationship(rel1)

        rel2 = UMLRelationship.UMLRelationship("temp", class3, class4)
        class3.add_relationship(rel2)
        class4.add_relationship(rel2)

        rel3 = UMLRelationship.UMLRelationship("temp", class1, class3)
        class1.add_relationship(rel3)
        class3.add_relationship(rel3)

        # ** end testing data **

    ######################################################################
    
    # **Write Documentation Here**
    def create_class(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def rename_class(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def delete_class(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def create_attribute(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def rename_attribute(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def delete_attribute(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def create_relationship(self):
        print ("To be implemented")

    ######################################################################
    
    # **Write Documentation Here**
    def delete_relationship(self):
        print ("To be implemented")

    ######################################################################
    
    # Saves the model's data to a given json filename
    # to be recovered for a future session 
    # @param filename - the name of a file to save the data 
    def save_model(self, filename):

        # object to hold JSON compatible version of the data
        raw_model = {}

        # grab class data 
        for name in self.classes:

            # raw data for the class
            raw_model[name] = {
                "name" : name,
                "attributes" : self.classes[name].attributes,
                "relationships" : []
            }

            # save relationships 
            for relationship in self.classes[name].relationships:
                # construct and add raw relationship
                raw_model[name]["relationships"] += [{
                    "name"   : relationship.name,
                    "class1" : relationship.class1.name,
                    "class2" : relationship.class2.name
                }]

        # Convert data into a JSON object
        json_data = json.dumps(raw_model, indent=4)

        # Open file and write json data
        with open(MODEL_DIRECTORY+filename, "w") as file:
            file.write(json_data)

        # Tell user that save was successful 
        print (f"Saved model to file {filename}")

    ######################################################################
    
    # **Write Documentation Here**
    def load_model(self):
        print ("To be implemented")

    ######################################################################

    # **Write Documentation Here**
    def list_class(self):
        print ("To be implemented")

    ######################################################################

    # **Write Documentation Here**
    def list_relationships(self):
        print ("To be implemented")


##########################################################################

