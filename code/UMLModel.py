# A representation of the state of a UML Model
# Description:     
#   This file keeps track of all the classes that are in the UML Model
#   It also handles saving/loading the Model to/from a JSON file 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 14 2020

##########################################################################
# Imports

import UMLClass
import UMLRelationship
import json
import os.path
from os import path

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

        # class1 = UMLClass.UMLClass("class1")
        # self.classes[class1.name] = class1
        # class1.add_attribute("A")
        # class1.add_attribute("B")
        # class1.add_attribute("C")
        # class2 = UMLClass.UMLClass("class2")
        # self.classes[class2.name] = class2
        # class2.add_attribute("D")
        # class2.add_attribute("E")
        # class2.add_attribute("F")
        # class3 = UMLClass.UMLClass("class3")
        # self.classes[class3.name] = class3
        # class3.add_attribute("G")
        # class4 = UMLClass.UMLClass("class4")
        # self.classes[class4.name] = class4
        # class4.add_attribute("N")
        # class4.add_attribute("I")
        # class4.add_attribute("C")
        # class4.add_attribute("E")

        # rel1 = UMLRelationship.UMLRelationship("r1", class2, class1)
        # class1.add_relationship(rel1)
        # class2.add_relationship(rel1)

        # rel2 = UMLRelationship.UMLRelationship("r2", class3, class4)
        # class3.add_relationship(rel2)
        # class4.add_relationship(rel2)

        # rel3 = UMLRelationship.UMLRelationship("r3", class1, class3)
        # class1.add_relationship(rel3)
        # class3.add_relationship(rel3)

        # ** end testing data **

    ######################################################################
    
    # Creates class object
    def create_class(self, name:str):
        # Checks to see if class already exists
        if name in self.classes:
            print("{} already exists.".format(name))
        else:
            # Creates class object and assigns it to a key
            self.classes[name] = UMLClass.UMLClass(name)

    ######################################################################
    
    # Renames an existing class object
    def rename_class(self, oldClassName:str, newClassName:str):
        # Checks if the old class name exists       
        if oldClassName not in self.classes:
            print("{} does not exist.".format(oldClassName))
        # Checks if the new class name is already in use 
        elif newClassName in self.classes:
            print("{} already exists.".format(newClassName))
        else:
            # Renames existing class object
            (self.classes[oldClassName]).name = newClassName
            # Assigns the renamed class object to a key with the new class name
            self.classes[newClassName] = self.classes.pop(oldClassName)

    ######################################################################
    
    # Deletes an existing class
    def delete_class(self, name:str):
        # Checks to see if specified class exists
        if name in self.classes:
            # Deletes key-value pair for specified class
            del self.classes[name]
            print("{} has been deleted.".format(name))
        else:
            print("{} does not exist.".format(name))

    ######################################################################
    
    # creates an attribute for an existing class
    def create_attribute(self, class_name:str, attribute_name:str):
        # checks if the the class exists
        if class_name in self.classes:
            # checks if the class does not have an attribute with the same name inputted
            if attribute_name not in self.classes[class_name].attributes:
                # creates attribute in class
                self.classes[class_name].attributes += [attribute_name]
                print("attribute {} has been created in {}".format(attribute_name, class_name))
            else:
                print("{} already exists in {}".format(attribute_name, class_name))   
        else:
            print("{} does not exist.".format(class_name))

    
    ######################################################################

    # Helper function to find an existing attribute
    # Returns index of attribute if it is found, -1 otherwise
    def find_attribute(self, class_name:str, attribute_name:str):
        for i in range(len(self.classes[class_name].attributes)):
            # Finds the attribute 
            if self.classes[class_name].attributes[i] == attribute_name:
                return i
        return -1    

    ######################################################################
    
    # renames an attribute for a given class
    def rename_attribute(self, class_name:str, old_attr_name:str, new_attr_name:str):
        # checks if the class exists
        if class_name not in self.classes:
            print("{} does not exist.".format(class_name))

        # checks if the attribute exists in the class
        elif old_attr_name not in self.classes[class_name].attributes:
            print("{} does not exist in {}.".format(old_attr_name, class_name))
        
        # checks if the inputted new attribute name already exists in the class
        elif new_attr_name in self.classes[class_name].attributes:    
            print("{} already exists in {}".format(new_attr_name, class_name))
                
        else:   
            # renames the attribute to new_attr_name
            index = self.find_attribute(class_name, old_attr_name)
            self.classes[class_name].attributes[index] = new_attr_name
            print("attribute {} has been renamed to {}".format(old_attr_name, new_attr_name))

    ######################################################################
    
    # Deletes an attribute for a given class
    def delete_attribute(self, class_name:str, attribute_name:str):
        # Check to see if given class exists
        # If it does...
        if class_name in self.classes:
            #finds position of attribute to delete
            index = self.find_attribute(class_name, attribute_name)
                    
            # if the attribute was not found
            if index != -1:
                # Delete the attribute
                self.classes[class_name].attributes.remove(attribute_name)

                # Give user verification that attribute was deleted
                print("{} has been deleted from {}".format(attribute_name, class_name))

                # Attribute has been found so exit loop
                return 

                # If the given attribute was not found, and we reached the end of our
                # list of attributes, tell the user that the attribute does not exit
            else: 
                print("{} is not an existing attribute in {}".format(attribute_name, class_name))
        else:
            # Tell the user the given class does not exist
            print("{} does not exist.".format(class_name))

       


    ######################################################################
    
    # **Write Documentation Here**
    def create_relationship(self, relationship_name:str, class_name1:str, class_name2:str):
        # Ensure first class exists
        if class_name1 not in self.classes:
            print (f"{class_name1} does not exist")
            return
        # Ensure second class exists
        if class_name2 not in self.classes:
            print (f"{class_name2} does not exist")
            return 

        # Ensure relationship does not already exist
        # we only have to check one of the classes
        for relationship in self.classes[class_name1].relationships:
            # found match
            if ((relationship.class1.name == class_name1 and relationship.class2.name == class_name2) or
                (relationship.class1.name == class_name2 and relationship.class2.name == class_name1)
                ):
                print(f"Relationship between {class_name1} and {class_name2} already exists.")
                return
        
        # does not find existing relationship
        # Ready to create and add relationship
        class1 = self.classes[class_name1]
        class2 = self.classes[class_name2]
        relationship = UMLRelationship.UMLRelationship(relationship_name, class1, class2)
        # add relationship to class objects
        class1.relationships += [relationship]
        class2.relationships += [relationship]

        # Prompt success
        print(f"Relationship between {class_name1} and {class_name2} was created")

    ######################################################################
    
    # **Write Documentation Here**
    def delete_relationship(self, class_name1:str, class_name2:str):
        # if class_name1 exist go to elif
        if class_name1 not in self.classes:
            print (f"{class_name1} does not exist")
        # if class_name1 exist go to else
        elif class_name2 not in self.classes:
            print (f"{class_name2} does not exist")
        else:
            # meaning that both classes exists and check the relationship
            # for the first class
            for rel in range(len(self.classes[class_name1].relationships)):
                # The relationship we are looking at
                relationship = self.classes[class_name1].relationships[rel]
                # find the relationship that is associate with class1
                if relationship.class1.name == class_name2 or relationship.class2.name == class_name2:
                    # delete the existing relationship between the first class and the second class
                    self.classes[class_name1].relationships.remove(relationship)
                    # For all of the existing relationships in the second class
                    for j in range(len(self.classes[class_name2].relationships)):
                        # relationship we are looking at in the second class
                        relationship2 = self.classes[class_name2].relationships[j]
                        # Find the relationship that is associated with the first class
                        # The first class may be stored as class1 or class2 for the relationship
                        # if it is, find it and delete it
                        if relationship2.class1.name == class_name1 or relationship2.class2.name == class_name1:
                            # Delete the existing relationship between the second class and the first class
                            self.classes[class_name2].relationships.remove(relationship2)
                            break
                    # The relationship has been deleted from both classes 
                    # Give the user varification that the relationship has been deleted
                    print(f"The relationship between {class_name1} and {class_name2} has been deleted")               
                    break
                if rel == len(self.classes[class_name1].relationships) - 1:
                    print(f"There is no exisiting relationship between {class_name1} and {class_name2}")

    ######################################################################
    
    # Saves the model's data to a given json filename
    # to be recovered for a future session 
    # @param filename - the name of a file to save the data 
    def save_model(self, filename):

        # Ensure file does not exist
        if path.exists(MODEL_DIRECTORY+filename):
            
            # continuously prompt until valid answer
            answer = ""
            while answer != "yes" and answer != "no":# prompt user if they want to overwrite or not
                print (f"File {filename} already exists.")
                print ("Do you want to overwrite the file? (yes/no)")

                answer = input().lower()

            if answer == "no":
                # cancel saving 
                print ("Saving FAILED")
                return


        # object to hold JSON compatible version of the data
        raw_model = {
            "classes" : {},
            "relationships" : []
        }

        # grab class data 
        for name in self.classes:

            # raw data for the class
            raw_model["classes"][name] = {
                "name" : name,
                "attributes" : self.classes[name].attributes
            }

        # save relationship data
        # tagging is used to make sure relationships are duplicated
        tag = 0
        for name in self.classes:
            for relationship in self.classes[name].relationships:
                # if relationship wasnt already tagged/visited
                if relationship.tag == -1:
                    relationship.tag = tag
                    tag += 1

                    # create and add relationship to raw_model
                    raw_model["relationships"] += [{
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
    
    # Loads the UML model from a given JSON file
    # NOTE - filename must be a file created by save_model
    # otherwise errors will be thrown
    def load_model(self, filename):

        # Clear out previous model
        self.classes = {}

        # Holds the data loaded from json
        raw_model = {}

        # Ensure file exists
        if not path.exists(MODEL_DIRECTORY+filename):
            print (f"{filename} does not exist")
            return

        # read json from file
        file = open(MODEL_DIRECTORY+filename, "r")
        raw_model = json.loads(file.read())
        file.close()

        # load classes (with attributes) into model
        for class_name in raw_model["classes"]:
            self.classes[class_name] = UMLClass.UMLClass(class_name)

            # add attributes to the class
            self.classes[class_name].attributes = raw_model["classes"][class_name]["attributes"]

        # load relationships 
        for rel in raw_model["relationships"]:
            # grab classes that are in the relationship
            c1 = self.classes[rel["class1"]]
            c2 = self.classes[rel["class2"]]
            # create relationship
            relationship = UMLRelationship.UMLRelationship(rel["name"],c1,c2)
            # add relationship to classes
            c1.add_relationship(relationship)
            c2.add_relationship(relationship)

        # Tell user load was successful
        print (f"Loaded model from {filename}")


    ######################################################################

    # Outputs all classes in the model 
    def list_classes(self):
        for class_name in self.classes:
            print (class_name)

    ######################################################################

    # Outputs all attributes for a given class
    def list_attributes(self, class_name:str):
        # Ensure class exists
        if class_name in self.classes:
            # loop the classes by the name 
            for i in range(len(self.classes[class_name].attributes)):
                attribute = self.classes[class_name].attributes[i]
                print(attribute)
        # not valid class
        else:
            print (f"{class_name} is not a class")

    ######################################################################

    # Outputs all of the relationships for a given class 
    # if class is not specified, all relationships are listed
    def list_relationships(self, class_name:str = ""):
        # list relationships for a specific class
        if class_name != "":
            # ensure class exists
            if class_name in self.classes:
                print (f"Relationships for {class_name}")
                # list all relationships for the class
                for relationship in self.classes[class_name].relationships:
                    if relationship.class1.name == class_name:
                        print (class_name,"---", relationship.name, "-->",relationship.class2.name)
                    else: 
                        print (class_name,"---", relationship.name, "-->",relationship.class1.name)

            # class_name is invalid
            else: 
                print (f"{class_name} does not exist")
        # list all relationships
        else:
            # for each class
            for class_name in self.classes:
                # for each relationship
                for relationship in self.classes[class_name].relationships:
                    # determine which class is the other 
                    if relationship.class1.name == class_name:
                        print (class_name,"---", relationship.name, "-->",relationship.class2.name)
                    else: 
                        print (class_name,"---", relationship.name, "-->",relationship.class1.name)

##########################################################################
