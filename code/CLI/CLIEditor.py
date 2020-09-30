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

from models.UMLModel import UMLModel
from . import CommandData

##########################################################################
# Constants 

# Colors for printing variation
PROMPT_COLOR  = "\033[1;36m"
ERROR_COLOR   = "\033[91m"
SUCCESS_COLOR = "\033[92m"
NORMAL_COLOR  = "\033[0;37m"

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
 
def print_help_message(model:UMLModel, command = ""):
    """Prints help message

    If an invalid command or no command is specified:
    - This prints out a list of all valid commands 

    Otherwise:
    - This prints out the usage and descriptions for the given command

    Params:
    - command (string) - the command to print information about

    """
    # if the command is valid 
    if command in CommandData.COMMANDS:
        # find usage info for command
        usages = CommandData.COMMANDS[command]
        # for each usage
        for usage in usages: 
            # print the usage
            print (usage["usage"])
            print ("\t", usage["desc"])
    # Print all commands
    elif command == "":
        print ("Type help <command_name> to see the usage of a command")
        # for each command
        for command in CommandData.COMMANDS:
            # print out the command
            print ("\t", command)
    # Invalid command
    else:
        print (f"{ERROR_COLOR}ArgumentError:{NORMAL_COLOR}",
                f"'{command}' is not a valid command")

##########################################################################

def execute(model:UMLModel, command:str, arguments:list = []):
    """Executes a given command with any arguments

    Params:
    - model (UMLModel) - the model to modify with commands
    - command (string) - a valid command to change the state of the model
    - arguments (list) - an optional list of arguments to supplement to 
        the command
    """
    # Ensure command is valid
    if command in CommandData.COMMANDS:
        # figure out which usage
        for usage in CommandData.COMMANDS[command]:
            # if the usage matches the num of args
            if usage["num_arguments"] == len(arguments):
                # call command with proper usage and arguments
                # *arguments uses the list as the parameters 
                usage["function"](model, *arguments)
                return True
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
            f"Incorrect usage of {command}\ntype 'help {command}' to see valid usages of {command}")
    else: 
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
            f"'{command}' is not a valid command\ntype 'help' for a list of valid commands")

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
            print ()
            exit()

        # User entered Interrupt
        except KeyboardInterrupt:
            print ("\nKeyboardInterrupt")

        # Tokenize user's input 
        words = user_input.split()

        # If user presses enter
        if len(words) == 0:
            continue
                    
        # This handles the case where there are no arguments
        execute(model, words[0], words[1:])

##########################################################################

# Program runs the REPL by default 
if __name__ == "__main__":
    REPL()
