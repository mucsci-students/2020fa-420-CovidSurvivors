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
from CommandData import COMMANDS

##########################################################################
# Constants 

# Colors for printing variation
PROMPT_COLOR = "\033[1;36m"
NORMAL_COLOR = "\033[0;37m"

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
        print(PROMPT_COLOR, "UMLEditor> ", NORMAL_COLOR, sep="", end="")

        # Read user's input
        user_input = input()

        # Tokenize user's input 
        words = user_input.split()

        # If user presses enter
        if len(words) == 0:
            continue
                    
        if words[0] in COMMANDS:
            # Case 0: Command has no arguments 
            if len(words) == 1:
                command = words[0]
                execute(model, command)

            # Case 1: Command has arguments 
            else:
                command, arguments = (words[0],words[1:])
                execute(model, command, arguments)
        else:
            print("Invalid command, type 'help' for information on commands")

##########################################################################

# Program runs the REPL by default 
if __name__ == "__main__":
    REPL()
