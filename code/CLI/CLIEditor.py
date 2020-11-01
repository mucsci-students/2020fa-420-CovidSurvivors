# A console-based UML editor interface
# Description:     
#   This file handles the input of the user and modifies the state
#   of the UML Model 
#   This file is the entry point into the UML Editor 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     November 1 2020

##########################################################################
# Imports

import cmd
from typing import Tuple 

from models.UMLModel import UMLModel
from . import CommandData
from command.command import CLICommand, Command, UndoableCLICommand
from command.command import CommandHistory

##########################################################################
# Constants 

# Colors for printing variation
PROMPT_COLOR  = "\033[1;36m"
ERROR_COLOR   = "\033[91m"
SUCCESS_COLOR = "\033[92m"
NORMAL_COLOR  = "\033[0m"
DESCRIPTION_COLOR = "\033[0;33m"

# The number of commands that are saved for undo-ing
HISTORY_LIMIT = 20

##########################################################################

class REPL(cmd.Cmd):
    """Read Eval Print Loop for the UMLEditor program

    A constantly running loop for the user to input commands to modify 
    the state of a UMLModel object. Uses tab completion from the cmd library.
    """
    intro = "This is the command-line interface for UMLEditor. \nPush 'Tab' to: view commands / help with completion."
    prompt = f"{PROMPT_COLOR}UMLEditor> {NORMAL_COLOR}"
    file = None

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.model = UMLModel()
        # Keeps track of the commands that were performed
        self.command_history = CommandHistory(HISTORY_LIMIT)
    
    def do_create_class(self, args):
        executeCMD(self.model, self.command_history, "create_class", args.split())

    def do_rename_class(self, args):
        executeCMD(self.model, self.command_history, "rename_class", args.split())

    def do_delete_class(self, args):
        executeCMD(self.model, self.command_history, "delete_class", args.split())

    def do_list_class(self, args):
        executeCMD(self.model, self.command_history, "list_class", args.split())

    def do_list_classes(self, args):
        executeCMD(self.model, self.command_history, "list_classes", args.split())

    def do_create_field(self, args):
        executeCMD(self.model, self.command_history, "create_field", args.split())
    
    def do_rename_field(self, args):
        executeCMD(self.model, self.command_history, "rename_field", args.split())

    def do_delete_field(self, args):
        executeCMD(self.model, self.command_history, "delete_field", args.split())

    def do_move_up_field(self, args):
        executeCMD(self.model, self.command_history, "move_up_field", args.split())

    def do_move_down_field(self, args):
        executeCMD(self.model, self.command_history, "move_down_field", args.split())

    def do_list_fields(self, args):
        executeCMD(self.model, self.command_history, "list_fields", args.split())

    def do_create_method(self, args):
        executeCMD(self.model, self.command_history, "create_method", args.split())

    def do_rename_method(self, args):
        executeCMD(self.model, self.command_history, "rename_method", args.split())

    def do_delete_method(self, args):
        executeCMD(self.model, self.command_history, "delete_method", args.split())

    def do_move_up_method(self, args):
        executeCMD(self.model, self.command_history, "move_up_method", args.split())

    def do_move_down_method(self, args):
        executeCMD(self.model, self.command_history, "move_down_method", args.split())

    def do_list_methods(self, args):
        executeCMD(self.model, self.command_history, "list_methods", args.split())

    def do_create_parameter(self, args):
        executeCMD(self.model, self.command_history, "create_parameter", args.split())

    def do_rename_parameter(self, args):
        executeCMD(self.model, self.command_history, "rename_parameter", args.split())

    def do_delete_parameter(self, args):
        executeCMD(self.model, self.command_history, "delete_parameter", args.split())                         

    def do_list_parameters(self, args):
        executeCMD(self.model, self.command_history, "list_parameters", args.split()) 

    def do_create_relationship(self, args):
        executeCMD(self.model, self.command_history, "create_relationship", args.split())
    
    def do_delete_relationship(self, args):
        executeCMD(self.model, self.command_history, "delete_relationship", args.split())
    
    def do_move_up_relationship(self, args):
        executeCMD(self.model, self.command_history, "move_up_relationship", args.split())
    
    def do_move_down_relationship(self, args):
        executeCMD(self.model, self.command_history, "move_down_relationship", args.split())

    def do_list_relationships(self, args):
        executeCMD(self.model, self.command_history, "list_relationships", args.split())

    def do_save_model(self, args):
        executeCMD(self.model, self.command_history, "save_model", args.split())

    def do_load_model(self, args):
        executeCMD(self.model, self.command_history, "load_model", args.split())

    def do_undo(self, args):
        undo(self.command_history, args.split())

    def do_redo(self, args):
        redo(self.command_history, args.split())

    def do_help(self, args):
        if args:
            print_help_message(self.model, args)
        else:
            print_help_message(self.model, "")

    def do_exit(self, args):
        prompt_exit(self.model)

    def complete_help(self, text, line, begidx, endidx):
        commands = list(CommandData.COMMANDS.keys())
        if text:
            return [
                command for command in commands
                if command.startswith(text)
            ]
        else:
            return commands

    # when user enters an empty command (pushes enter)
    def emptyline(self):
         pass

    def do_EOF(self, args):
        print()
        return True

    def default(self, line):
        """Outputs a message when the command prefix cannot be matched"""
        print(f"{ERROR_COLOR}CommandError:{NORMAL_COLOR} Unknown command '{line.split()[0]}'")

##########################################################################

def runCMD():
    """ Runs the REPL """
    # store repl so we can save it's state between each loop
    repl = REPL()
    while True:
        try:
            repl.cmdloop()
            # cmdloop ended normally
            # exit program
            break
        except KeyboardInterrupt:
            # remove intro message
            # so it does not display again
            repl.intro = ""
            # print a newline so the prompt displays on
            # the next line 
            print()
            print("KeyboardInterrupt")
            # re-run the cmd loop 

##########################################################################

def executeCMD(model:UMLModel, command_history:CommandHistory, commandName:str, arguments:list) -> None:
    """Grabs the command and pushes it into the history if it is undoable
    Executes the command in the REPL, and prints out a success/error message
    depending on whether it was an appropriate command
    
    Params:
    - model - the current model to execute commands on 
    - commandName - the name of the command
    - arguments - the possible argument(s) that came with the command
    """
    
    # Ensure valid command
    if commandName not in CommandData.COMMANDS:
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
            f"'{commandName}' is not a valid command\ntype 'help' for a list of valid commands")
        return
    
    # Find command usage matching args
    # and validate number of arguments
    command = None
    for usage in CommandData.COMMANDS[commandName]:
        # found usage matching num args
        if usage["num_arguments"] == len(arguments):
            # if the command class was provided
            if "command" in usage:
                command = usage["command"](model, usage["function"], arguments)
            # otherwise, assume it is not an undoable command
            else:
                command = CLICommand(model, usage["function"], arguments)
            break
    # matching usage not found
    else:
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
            f"Incorrect usage of {commandName}\ntype 'help {commandName}' to see valid usages of {commandName}")
        return 

    # save backup - for undoable commands
    if isinstance(command, UndoableCLICommand):
        command.saveBackup()

    # execute the command
    status, msg = command.execute()

    # Ensure command was successful
    if not status:
        print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")
        return

    # push undoable commands to the history
    if isinstance(command, UndoableCLICommand):
        # add to the list of history
        command_history.push(command)

    print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")

##########################################################################
 
def print_help_message(model:UMLModel, command = "") -> None:
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
            print ("Usage:")
            print (f"  {DESCRIPTION_COLOR}{usage['usage']}{NORMAL_COLOR}")
            print ("Description:")
            print (f"  {usage['desc']}")
    # Print all commands
    elif command == "":
        print ("Type help <command_name> to see the usage of a command")
        # for each command
        for command in CommandData.COMMANDS:
            # print out the command
            print ("\t", command)
            usages = CommandData.COMMANDS[command]
            # for each usage
            for usage in usages:
                if usage["skip_line"] == True:
                    print()
    # Invalid command
    else:
        print(f"{ERROR_COLOR}ArgumentError:{NORMAL_COLOR} "
                f"'{command}' is not a valid command")

##########################################################################

def prompt_exit(model:UMLModel) -> Tuple[bool, str]:
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
        return (True, "Exit aborted")

    elif response == "no":
        print("Goodbye!")

    exit()

##########################################################################

def undo(command_history:CommandHistory, args:list):
    """Undoes a command in the given command history and prints whether 
    it was successful or not. the args parameter just checks to make sure
    no arguments were provided
    """
    # Ensure no args 
    if len(args) != 0:
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
        f"Incorrect usage of undo\nundo does not take any arguments")
        return 

    # get undoable command
    command = command_history.pop_undo()

    # ensure there was a command
    if command == None:
        print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} no command to undo")
        return
    
    # undo the command
    command.undo()

    print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} command undone succesfully")

##########################################################################

def redo(command_history:CommandHistory, args:list):
    """redoes a command in the given command history and prints whether 
    it was successful or not. the args parameter just checks to make sure
    no arguments were provided
    """
    # Ensure no args 
    if len(args) != 0:
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
        f"Incorrect usage of redo\nredo does not take any arguments")
        return  

    # get undone command
    command = command_history.pop_redo()

    # ensure there was a command
    if command == None:
        print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} no command to redo")
        return
    
    # redo the command
    command.execute()

    print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} command redone succesfully")

##########################################################################

# Program runs the REPL by default 
if __name__ == "__main__":
    runCMD()

