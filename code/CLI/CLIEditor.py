# A console-based UML editor interface
# Description:     
#   This file handles the input of the user and modifies the state
#   of the UML Model 
#   This file is the entry point into the UML Editor 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 16 2020

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
# Globals

# Keeps track of the commands that were performed
command_history = CommandHistory(HISTORY_LIMIT)

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
            print (f"{DESCRIPTION_COLOR}",usage["usage"])
            print ("\t", f"{NORMAL_COLOR}", usage["desc"])
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

def undo(model:UMLModel) -> Tuple[bool, str]:

    # get undoable command
    command = command_history.pop_undo()

    # ensure there was a command
    if command == None:
        return (False, "No command to undo")
    
    # undo the command
    command.undo()

    return (True, "undid command")

##########################################################################

def redo(model:UMLModel) -> Tuple[bool, str]:

    # get undone command
    command = command_history.pop_redo()

    # ensure there was a command
    if command == None:
        return (False, "No command to redo")
    
    # redo the command
    command.execute()

    return (True, "redid command")

##########################################################################

def getCommand(model:UMLModel, command:str, arguments:list = []) -> Command:
    """Returns the matching command with any arguments

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
                # construct command
                return usage["command"](model, usage["function"], arguments)
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
            f"Incorrect usage of {command}\ntype 'help {command}' to see valid usages of {command}")
    else: 
        print (f"{ERROR_COLOR}CommandError:{NORMAL_COLOR}",
            f"'{command}' is not a valid command\ntype 'help' for a list of valid commands")

##########################################################################

class REPL(cmd.Cmd):
    """Read Eval Print Loop for the UMLEditor program

    A constantly running loop for the user to input commands to modify 
    the state of a UMLModel object. 
    """
    intro = "This is the command-line interface for UMLEditor. \nPush 'Tab' to: view commands / help with completion."
    prompt = f"{PROMPT_COLOR}UMLEditor> {NORMAL_COLOR}"
    file = None
    # Keep a representation of the UML model 
    global model
    model = UMLModel()
    
    def do_create_class(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "create_class", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_rename_class(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "rename_class", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_delete_class(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "delete_class", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_list_class(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "list_class", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_list_classes(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "list_classes", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_create_field(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "create_field", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")
    
    def do_rename_field(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "rename_field", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_delete_field(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "delete_field", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_move_up_field(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "move_up_field", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_move_down_field(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "move_down_field", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_list_fields(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "list_fields", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_create_method(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "create_method", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_rename_method(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "rename_method", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_delete_method(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "delete_method", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_move_up_method(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "move_up_method", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_move_down_method(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "move_down_method", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_list_methods(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "list_methods", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_create_parameter(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "create_parameter", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}") 

     def do_rename_parameter(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "rename_parameter", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")                      

    def do_list_parameters(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "list_parameters", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}") 

    def do_create_relationship(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "create_relationship", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")
    
    def do_delete_relationship(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "delete_relationship", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")
    
    def do_move_up_relationship(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "move_up_relationship", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")
    
    def do_move_down_relationship(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "move_down_relationship", words[0:])
        # save backup
        command.saveBackup()
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # Ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
                # Undoable Commands 
                if isinstance(command, UndoableCLICommand):
                    # add to the list of history
                    command_history.push(command)
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_list_relationships(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "list_relationships", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_save_model(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "save_model", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_load_model(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "load_model", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_undo(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "undo", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_redo(self, args):
        words = args.split()
        # grab the command
        # this handles the case where there are no arguments
        command = getCommand(model, "redo", words[0:])
        # execute the command
        response = command.execute()
        # ensure there was a response
        if response:
            status, msg = response
            # ensure command was successful
            if status:
                print(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR} {msg}")
            else:
                print(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} {msg}")

    def do_help(self, args):
        if args:
            print_help_message(model, args)
        else:
            print_help_message(model, "")

    def do_exit(self, args):
        prompt_exit(model)

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
##########################################################################

# store repl so we can save it's state between runCMD() calls
repl = REPL()
def runCMD():
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

# Program runs the REPL by default 
if __name__ == "__main__":
    runCMD()

