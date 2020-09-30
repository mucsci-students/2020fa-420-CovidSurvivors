# Data for the commands of the UML Editor
# Description:     
#   This file constructs the data structure for 
#   the commands and their usages and descriptions 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

import UMLEditor
import UMLModel

# Data structure for storing all of the valid commands
#   and any extra information to give to the user 
COMMANDS = {
    "help" : [
        {
            "usage" : "help", 
            "desc" : "lists all possible commands",
            "function" : UMLEditor.print_help_message,
            "num_arguments" : 0
        },
        {
            "usage" : "help <command_name>", 
            "desc" : "lists the usage for <command_name>",
            "function" : UMLEditor.print_help_message,
            "num_arguments" : 1
        }
    ],
    "exit" : [
        {
            "usage" : "exit",
            "desc" : "exits the program",
            "function" : UMLEditor.prompt_exit,
            "num_arguments" : 0
        }
    ],
    "create_class" : [
        {
            "usage" : "create_class <class_name>",
            "desc" : "creates a class named <class_name> and adds it to the model",
            "function" : UMLModel.UMLModel.create_class,
            "num_arguments" : 1 
        }
    ],
    "rename_class" : [
        {
            "usage" : "rename_class <old_name> <new_name>",
            "desc" : "renames the class <old_name> with the <new_name>",
            "function" : UMLModel.UMLModel.rename_class,
            "num_arguments" : 2
        }
    ],
    "delete_class" : [
        {
            "usage" : "delete_class <class_name>",
            "desc" : "deletes the class with the name <class_name> from the model",
            "function" : UMLModel.UMLModel.delete_class,
            "num_arguments" : 1
        }
    ],
    "create_field" : [
        {
            "usage" : "create_field <class_name> <visibility> <field_name> <field_type>",
            "desc" : "creates a field named <field_name> of type <field_type> and adds it to the given class \n <visibility> determines if the field is public/private,",
            "function" : UMLModel.UMLModel.create_field,
            "num_arguments" : 4
        }
    ],
    "rename_field" : [
        {
            "usage" : "rename_field <class_name> <old_name> <new_name>",
            "desc" : "renames the attribute <old_name> with the <new_name> for the class, <class_name>",
            "function" : UMLModel.UMLModel.rename_field,
            "num_arguments" : 3
        }
    ],
    "delete_field" : [
        {
            "usage" : "delete_attribute <class_name> <attrib_name>",
            "desc" : "deletes the attribute from the class",
            "function" : UMLModel.UMLModel.delete_field,
            "num_arguments" : 2
        }
    ],
    "create_relationship" : [
        {
            "usage" : "create_relationship <relationship_type> <class1> <class2>",
            "desc" : "creates a relationship between <class1> and <class2>",
            "function" : UMLModel.UMLModel.create_relationship,
            "num_arguments" : 3
        }
    ],
    "delete_relationship" : [
        {
            "usage" : "delete_relationship <class1> <class2>",
            "desc" : "removes the relationship between <class1> and <class2>",
            "function" : UMLModel.UMLModel.delete_relationship,
            "num_arguments" : 2
        }
    ],
    "save_model" : [
        {
            "usage" : "save_model <filename>",
            "desc" : "saves the UMLModel into <filename> as JSON",
            "function" : UMLModel.UMLModel.save_model,
            "num_arguments" : 1
        }
    ],
    "load_model" : [
        {
            "usage" : "load_model <filename>",
            "desc" : "loads the UMLModel from <filename> and uses it as the working UMLModel",
            "function" : UMLModel.UMLModel.load_model,
            "num_arguments" : 1
        }
    ],
    "list_classes" : [
        {
            "usage" : "list_classes",
            "desc" : "prints out the name of all classes in the model",
            "function" : UMLModel.UMLModel.list_classes,
            "num_arguments" : 0
        }
    ],
    "list_fields" : [
        {
            "usage" : "list_fields <class_name>",
            "desc" : "prints all of the fields for a given class",
            "function" : UMLModel.UMLModel.list_fields,
            "num_arguments" : 1
        }
    ],
    "list_relationships" : [
        {
            "usage" : "list_relationships",
            "desc" : "prints out the classes that each class relate to",
            "function" : UMLModel.UMLModel.list_relationships,
            "num_arguments" : 0
        },
        {
            "usage" : "list_relationships <class_name>",
            "desc" : "prints out the classes that a relate to class_name",
            "function" : UMLModel.UMLModel.list_relationships,
            "num_arguments" : 1
        }
    ]

}