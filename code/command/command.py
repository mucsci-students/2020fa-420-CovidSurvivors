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
from typing import Tuple

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

    def execute(self) -> Tuple[bool, str]:
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

    def execute(self) -> Tuple[bool, str]:
        # the payload stores just the class name
        return self.receiver_function(self.model, *self.arguments)

##########################################################################

# This is for the GUI
class CreateClassGUICommand(Command, Undoable):

    def __init__(self, model, payload):
        self.model = model
        self.payload = payload
        self.backup = None
    
    def saveBackup(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # save state
        self.backup = self.model.get_data()

    def undo(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # restore state
        self.model.set_data(self.backup)
        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

    def execute(self) -> bool:
        # Load model to
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        
        # Ensure class does not already exist
        if self.payload["class_name"] in self.model.classes:
            return False, f"{self.payload['class_name']} already exists"

        # create the class
        self.model.create_class(self.payload["class_name"])

        # add the fields
        for i in range(len(self.payload["field_names"])):
            self.model.create_field(self.payload["class_name"], self.payload["field_visibilities"][i].lower(), self.payload["field_types"][i], self.payload["field_names"][i])

        # add the methods
        for i in range(len(self.payload["method_names"])):
            self.model.create_method(self.payload["class_name"], self.payload["method_visibilities"][i].lower(), self.payload["method_types"][i], self.payload["method_names"][i])

        # add the parameters
        for i in range(len (self.payload["parameter_names"])): 
            self.model.create_parameter(self.payload["class_name"], self.payload["method_names"][int(self.payload["parameter_method_index"][i])], self.payload["parameter_types"][i], self.payload["parameter_names"][i])   

        # add relationships
        for i in range(len(self.payload["relationship_types"])):
            self.model.create_relationship(self.payload["relationship_types"][i].lower(), self.payload["class_name"], self.payload["relationship_others"][i])

        self.model.list_class(self.payload["class_name"])

        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

        return True, f"{self.payload['class_name']} was created successfully"

##########################################################################

# This is for the GUI
class EditClassGUICommand(Command, Undoable):

    def __init__(self, model, payload):
        self.model = model
        self.payload = payload
        self.backup = None
    
    def saveBackup(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # save state
        self.backup = self.model.get_data()

    def undo(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # restore state
        self.model.set_data(self.backup)
        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

    def execute(self) -> bool:
        # Load model 
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        
        # Ensure it was an existing class
        if self.payload["original_name"] not in self.model.classes:
            return False, f"{self.payload['original_name']} is not a valid class"

        # remove the original class to replace it
        self.model.delete_class(self.payload["original_name"])

        # create the class
        status, msg = self.model.create_class(self.payload["class_name"])

        # ensure new class was created successfully 
        # this fails if the user entered a new name that already exists
        if not status:
            return status, msg

        # add the fields
        for i in range(len(self.payload["field_names"])):
            self.model.create_field(self.payload["class_name"], self.payload["field_visibilities"][i].lower(), self.payload["field_types"][i], self.payload["field_names"][i])

        # add the methods
        for i in range(len(self.payload["method_names"])):
            self.model.create_method(self.payload["class_name"], self.payload["method_visibilities"][i].lower(), self.payload["method_types"][i], self.payload["method_names"][i])

        # add the parameters
        for i in range(len(self.payload["parameter_names"])): 
            self.model.create_parameter(self.payload["class_name"], self.payload["method_names"][int(self.payload["parameter_method_index"][i])], self.payload["parameter_types"][i], self.payload["parameter_names"][i])   

        # add relationships
        for i in range(len(self.payload["relationship_types"])):
            self.model.create_relationship(self.payload["relationship_types"][i].lower(), self.payload["class_name"], self.payload["relationship_others"][i])

        self.model.list_class(self.payload["class_name"])

        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

        return True, "Class was updated successfully"

##########################################################################

# This is for the GUI
class DeleteClassGUICommand(Command, Undoable):

    def __init__(self, model, payload):
        self.model = model
        self.payload = payload
        self.backup = None
    
    def saveBackup(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # save state
        self.backup = self.model.get_data()

    def undo(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # restore state
        self.model.set_data(self.backup)
        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

    def execute(self) -> bool:
        # Load model to delete class
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # delete class
        status, msg = self.model.delete_class(self.payload["class_name"])
        
        # delete failed
        if not status:
            return status, msg
        
        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

        return True, f"{self.payload['class_name']} was deleted"

##########################################################################

# This is for the GUI
class SetClassPositonGUICommand(Command, Undoable):

    def __init__(self, model, payload):
        self.model = model
        self.payload = payload
        self.backup = None
    
    def saveBackup(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # save state
        self.backup = self.model.get_data()

    def undo(self) -> None:
        # Load model
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # restore state
        self.model.set_data(self.backup)
        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

    def execute(self) -> bool:
        # Load model to set class position
        self.model.load_model(self.payload["filename"], directory=self.payload["directory"])
        # set position of class
        status, msg = self.model.set_class_position(self.payload["class_name"], self.payload["x"], self.payload["y"], self.payload["zindex"])

        # save model
        self.model.save_model(self.payload["filename"], directory=self.payload["directory"])

        return True, f"The position of {self.payload['class_name']} has been set to ({self.payload['x']}, {self.payload['y']}) with a z-index of {self.payload['zindex']}."
