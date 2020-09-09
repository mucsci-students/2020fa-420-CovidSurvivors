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

# **Write Documentation Here**
def prompt_exit():
    print ("To be implemented")

##########################################################################

# **Write Documentation Here**
def print_help_message():
    print ("To be implemented")

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
