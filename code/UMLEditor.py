# A console-based UML editor interface
# Description:     
#   This file handles the input of the user and modifies the state
#   of the UML Model 
#   This file is the entry point into the UML Editor 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

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

def prompt_exit(model:UMLModel):
    """Initiates the exit prompt

    Prompts user if they want to save before quitting
    
    If user types 'yes':
    - User is prompted for a filename to save to 
    - Model is saved 
    - Program exits
    
    If user types 'no':
    - program exits without saving 

    If user types 'cancel':
    - model is not saved
    - returns from this function

    Params:
    - model (UMLModel) - the model to optionally save 
    """

    response = ""
    # Prompt user until we get a valid answer
    while response != "yes" and response != "no" and response != "cancel":
        print("Do you want to save current working project? (yes/no/cancel)")
        response = input().lower()
        
    # if user wants to save project, call the save_model function to save working project 
    if response == "yes":
        print("Please enter the filename.")
        filename = input()
        model.save_model(filename)

    elif response == "cancel":
        return

    elif response == "no":
        print("Goodbye!")

    exit()
    
##########################################################################
 
def print_help_message(command = ""):
    """Prints help message

    If an invalid command or no command is specified:
    - This prints out a list of all valid commands 

    Otherwise:
    - This prints out the usage and descriptions for the given command

    Params:
    - command (string) - the command to print information about

    """

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

def execute(model:UMLModel, command:str, arguments:list = []):
    """Executes a given command with any arguments

    Params:
    - model (UMLModel) - the model to modify with commands
    - command (string) - a valid command to change the state of the model
    - arguments (list) - an optional list of arguments to supplement to 
        the command
    """
    try:
        if(command == "help"):
            # if there are no arguments next to the command
            if not arguments:
                print_help_message()
            else:
                print_help_message(arguments[0])
        elif(command == "exit"):
            prompt_exit(model)
        # For all the commands, the corresponding functions are pulled from UMLModel.py
        elif(command == "create_class"):
            model.create_class(arguments[0])
        elif(command == "rename_class"):
            model.rename_class(arguments[0], arguments[1])
        elif(command == "delete_class"):
            model.delete_class(arguments[0])
        elif(command == "create_attribute"):
            model.create_attribute(arguments[0], arguments[1])
        elif(command == "rename_attribute"):
            model.rename_attribute(arguments[0], arguments[1], arguments[2])
        elif(command == "delete_attribute"):
            model.delete_attribute(arguments[0], arguments[1])
        elif(command == "create_relationship"):
            model.create_relationship(arguments[0], arguments[1], arguments[2])
        elif(command == "delete_relationship"):
            model.delete_relationship(arguments[0], arguments[1])
        elif(command == "save_model"):
            model.save_model(arguments[0])
        elif(command == "load_model"):
            model.load_model(arguments[0])
        elif(command == "list_classes"):
            model.list_classes()
        elif(command == "list_attributes"):
            model.list_attributes(arguments[0])
        elif(command == "list_relationships"):
            # if there are no arguments next to the command
            if not arguments:
                model.list_relationships()
            else:
                model.list_relationships(arguments[0])
    except IndexError:
        print("Invalid arguments for {}, type 'help {}' for information on {}".format(command, command, command))              

##########################################################################

def REPL():
    """Read Eval Print Loop for the UMLEditor program

    A constantly running loop for the user to input commands to modify 
    the state of a UMLModel object. 
    """
    # Keep a representation of the UML model 
    model : UMLModel = UMLModel()

    while (True):

        # Give user a prompt 
        print(PROMPT_COLOR, "UMLEditor> ", NORMAL_COLOR, sep="", end="")

        # Read user's input
        try:
            user_input = input()

        # User entered EOF character
        # Ctrl + D
        except EOFError:
            print ("\nEOF entered - Exiting")
            prompt_exit(model)

        # User entered Interrupt
        except KeyboardInterrupt:
            print ("\nKeyboardInterrupt - Exiting")
            prompt_exit(model)

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
                # test for create_attribute (does not work at the moment):
                # UMLModel.create_attribute = (self.attributes, arguments[0], arguments[1])
                execute(model, command, arguments)
        else:
            print("Invalid command, type 'help' for information on commands")

##########################################################################

# Program runs the REPL by default 
if __name__ == "__main__":
    REPL()
