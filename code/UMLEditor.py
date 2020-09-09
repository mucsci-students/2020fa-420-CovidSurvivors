# A console-based UML editor interface
# Description:     
#   This file handles the input of the user and modifies the state
#   of the UML Model 
#   This file is the entry point into the UML Editor 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 8 2020

##########################################################################
# Imports

from UMLModel import UMLModel
import UMLClass
import UMLRelationship

##########################################################################
# Constants 

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
    "list_class" : [
        {
            "usage" : "list_class <class_name>",
            "desc" : "prints all of the attributes for a given class"
        }
    ],
    "list_relationships" : [
        {
            "usage" : "list_relationships",
            "desc" : "prints out the classes that each class relate to"
        }
    ]

}

##########################################################################

# **Write Documentation Here**
def prompt_exit():
    print ("To be implemented")

##########################################################################

# Prints the list of valid commands
# or it prints out the usage for a given command
# NOTE if the inputted command is not a valid command
#   then it prints out all of the possible commands  
def print_help_message(command = ""):

    # if the command is valid 
    if command in COMMANDS:
        # find usage info for command
        usages = COMMANDS[command]
        # for each usage
        for usage in usages: 
            # print the usage
            print (usage["usage"])
            print ("\t", usage["desc"])
    # Print all commands
    else:
        print ("Type help <command_name> to see the usage of a command")
        # for each command
        for command in COMMANDS:
            # print out the command
            print ("\t", command)

##########################################################################

# **Write Documentation Here**
def execute(model:UMLModel, command:str, arguments:list = []):
    print ("To be implemented")

##########################################################################

# Runs and processes each command given by a user
def REPL():

    # Keep a representation of the UML model 
    model : UMLModel = UMLModel()

    while (True):

        # Give user a prompt 
        print(">", end="")

        # Read user's input
        user_input = input()

        # Tokenize user's input 
        words = user_input.split()

        # Case 0: user presses enter
        if len(words) == 0:
            continue

        # Case 1: Command has no arguments 
        if len(words) == 1:
            command = words[0]
            execute(model, command)

        # Case 2: Command has arguments 
        else:
            command, arguments = (words[0],words[1:])
            execute(model, command, arguments)

##########################################################################

# Program runs the REPL by default 
if __name__ == "__main__":
    REPL()
