# Data for the commands of the UML Editor
# Description:     
#   This file constructs the data structure for 
#   the commands and their usages and descriptions 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 13 2020


# Data structure for storing all of the valid commands
#   and any extra information to give to the user 
COMMANDS = {
    "help" : [
        {
            "usage" : "help", 
            "desc" : "lists all possible commands"
        },
        {
            "usage" : "help <command_name>", 
            "desc" : "lists the usage for <command_name>"
        }
    ],
    "exit" : [
        {
            "usage" : "exit",
            "desc" : "exits the program"
        }
    ],
    "create_class" : [
        {
            "usage" : "create_class <class_name>",
            "desc" : "creates a class named <class_name> and adds it to the model"
        }
    ],
    "rename_class" : [
        {
            "usage" : "rename_class <old_name> <new_name>",
            "desc" : "renames the class <old_name> with the <new_name>"
        }
    ],
    "delete_class" : [
        {
            "usage" : "delete_class <class_name>",
            "desc" : "deletes the class with the name <class_name> from the model"
        }
    ],
    "create_attribute" : [
        {
            "usage" : "create_attribute <class_name> <attrib_name>",
            "desc" : "creates an attribute named <class_name> and adds it to the given class"
        }
    ],
    "rename_attribute" : [
        {
            "usage" : "rename_attribute <class_name> <old_name> <new_name>",
            "desc" : "renames the attribute <old_name> with the <new_name> for the class, <class_name>"
        }
    ],
    "delete_attribute" : [
        {
            "usage" : "delete_attribute <class_name> <attrib_name>",
            "desc" : "deletes the attribute from the class"
        }
    ],
    "create_relationship" : [
        {
            "usage" : "create_relationship <class1> <class2>",
            "desc" : "creates a relationship between <class1> and <class2>"
        }
    ],
    "delete_relationship" : [
        {
            "usage" : "delete_relationship <class1> <class2>",
            "desc" : "removes the relationship between <class1> and <class2>"
        }
    ],
    "save_model" : [
        {
            "usage" : "save_model <filename>",
            "desc" : "saves the UMLModel into <filename> as JSON"
        }
    ],
    "load_model" : [
        {
            "usage" : "load_model <filename>",
            "desc" : "loads the UMLModel from <filename> and uses it as the working UMLModel"
        }
    ],
    "list_classes" : [
        {
            "usage" : "list_classes",
            "desc" : "prints out the name of all classes in the model"
        }
    ],
    "list_attributes" : [
        {
            "usage" : "list_attributes <class_name>",
            "desc" : "prints all of the attributes for a given class"
        }
    ],
    "list_relationships" : [
        {
            "usage" : "list_relationships",
            "desc" : "prints out the classes that each class relate to"
        },
        {
            "usage" : "list_relationships <class_name>",
            "desc" : "prints out the classes that a relate to class_name"
        }
    ]

}