# Command Design Pattern Implementation
# Description:     
#   This file follows the Command Design Pattern to separate the execution
#   of commands 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 16 2020

##########################################################################
# Imports

from abc import ABC, abstractmethod

##########################################################################
# Main Inherited Command Class

class Command(ABC):

    @abstractmethod
    def execute(self) -> bool:
        pass

class Undoable(ABC):

    @abstractmethod
    def undo(self) -> None:
        pass

class CommandHistory:

    def __init__(self, limit:int):
        self.limit = limit
        self.history = []
        self.future = []

    def push(self, command:Command) -> None:
        """Adds the given command to the history
        """
        self.history.append(command)
        # ensure history doesnt exceed the limit
        if len(self.history) > self.limit:
            # remove last in the history list
            self.history.pop(0)
        # clear future list
        self.future = []

    def pop_undo(self) -> Command:
        """Removes and returns a command that was executed

        NOTE: the command is saved in a redo list to be redone
        """
        # ensure there are things to undo
        if len(self.history) == 0:
            return None 

        # move command from top of history to future list
        command = self.history.pop()
        self.future.append(command)

        # ensure future doesnt exceed the limit 
        if len(self.future) > self.limit:
            # remove last in the future list
            self.future.pop(0)

        return command

    def pop_redo(self) -> Command:
        """Removes and returns a command that was previously undone
        """
        # ensure there are things to redo
        if len(self.future) == 0:
            return None

        # move future command to history
        command = self.future.pop()
        self.history.append(command)

        # ensure history doesnt exceed the limit
        if len(self.history) > self.limit:
            # remove last in the history list
            self.history.pop(0)

        return command

##########################################################################

class UndoableCLICommand(Command, Undoable):
    """
    Acts as a command for any type of CLI Command
    Allows for the delayed execution of this command
    Allows for this command to be undone
    """

    def __init__(self, model, receiver_function, arguments):
        self.model = model
        self.receiver_function = receiver_function 
        self.arguments = arguments
        self.backup = None

    def saveBackup(self) -> None:
        self.backup = self.model.get_data()
    
    def undo(self) -> None:
        self.model.set_data(self.backup)

    def execute(self) -> bool:
        # the payload stores just the class name
        return self.receiver_function(self.model, *self.arguments)

##########################################################################

class CLICommand(Command):
    """
    Acts as a command for any type of CLI Command
    Allows for the delayed execution of this command
    This does not support undo
    """

    def __init__(self, model, receiver_function, arguments):
        self.model = model
        self.receiver_function = receiver_function 
        self.arguments = arguments

    def execute(self) -> bool:
        # the payload stores just the class name
        return self.receiver_function(self.model, *self.arguments)