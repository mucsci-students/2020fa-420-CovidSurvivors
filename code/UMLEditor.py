# This file

##########################################################################

# from UMLModel import UMLModel

##########################################################################

def prompt_exit():
    print ("To be implemented")

##########################################################################

def print_help_message():
    print ("To be implemented")

##########################################################################

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

if __name__ == "__main__":
    REPL()
