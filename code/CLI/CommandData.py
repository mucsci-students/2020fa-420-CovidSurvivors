# Data for the commands of the UML Editor
# Description:     
#   This file constructs the data structure for 
#   the commands and their usages and descriptions 
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20 2020

from . import CLIEditor
from models.UMLModel import UMLModel
from command.command import UndoableCLICommand, CLICommand

# Data structure for storing all of the valid commands
#   and any extra information to give to the user 
COMMANDS = {
    "create_class" : [
        {
            "usage" : "create_class <class_name>",
            "desc" : "creates a class named <class_name> and adds it to the model",
            "command" : UndoableCLICommand,
            "function" : UMLModel.create_class,
            "num_arguments" : 1, 
            "skip_line" : False
        }
    ],
    "rename_class" : [
        {
            "usage" : "rename_class <old_name> <new_name>",
            "desc" : "renames the class <old_name> with the <new_name>",
            "command" : UndoableCLICommand,
            "function" : UMLModel.rename_class,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],
    "delete_class" : [
        {
            "usage" : "delete_class <class_name>",
            "desc" : "deletes the class with the name <class_name> from the model",
            "command" : UndoableCLICommand,
            "function" : UMLModel.delete_class,
            "num_arguments" : 1,
            "skip_line" : False
        }
    ],
    "list_class" : [
        {
            "usage" : "list_class <class_name>",
            "desc" : "prints out all components of the <class_name>",
            "command" : CLICommand,
            "function" : UMLModel.list_class,
            "num_arguments" : 1,
            "skip_line" : False
        }
    ],
    "list_classes" : [
        {
            "usage" : "list_classes",
            "desc" : "prints out the name of all classes in the model",
            "command" : CLICommand,
            "function" : UMLModel.list_classes,
            "num_arguments" : 0,
            "skip_line" : True
        }
    ],
    "create_field" : [
        {
            "usage" : "create_field <class_name> <visibility> <field_type> <field_name>",
            "desc" : "creates a field named <field_name> of type <field_type> and adds it to the given class \n <visibility> determines if the field is public/private,",
            "command" : UndoableCLICommand,
            "function" : UMLModel.create_field,
            "num_arguments" : 4,
            "skip_line" : False
        }
    ],
    "rename_field" : [
        {
            "usage" : "rename_field <class_name> <old_name> <new_name>",
            "desc" : "renames the attribute <old_name> with the <new_name> for the class, <class_name>",
            "command" : UndoableCLICommand,
            "function" : UMLModel.rename_field,
            "num_arguments" : 3,
            "skip_line" : False
        }
    ],
    "delete_field" : [
        {
            "usage" : "delete_field <class_name> <attrib_name>",
            "desc" : "deletes the field from the class",
            "command" : UndoableCLICommand,
            "function" : UMLModel.delete_field,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],
    "move_up_field" : [
        {
            "usage" : "move_up_field <class_name> <field_name>",
            "desc" : "moves field up one space in a list of fields",
            "command" : UndoableCLICommand,
            "function" : UMLModel.move_up_field,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],
    "move_down_field" : [
        {
            "usage" : "move_down_field <class_name> <field_name>",
            "desc" : "moves field down one space in a list of foe;ds",
            "command" : UndoableCLICommand,
            "function" : UMLModel.move_down_field,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],  
    "list_fields" : [
        {
            "usage" : "list_fields <class_name>",
            "desc" : "prints all of the fields for a given class",
            "command" : CLICommand,
            "function" : UMLModel.list_fields,
            "num_arguments" : 1,
            "skip_line" : True
        }
    ],
     "create_method" : [
        {
            "usage" : "create_method <class_name> <visibility> <method_type> <method_name>",
            "desc" : "creates a method named <method_name> of type <method_type> and adds it to the given class \n <visibility> determines if the method is public/private,",
            "command" : UndoableCLICommand,
            "function" : UMLModel.create_method,
            "num_arguments" : 4,
            "skip_line" : False
        }
    ],
    "rename_method" : [
        {
            "usage" : "rename_method <class_name> <old_name> <new_name>",
            "desc" : "renames the method <old_name> with the <new_name> for the class, <class_name>",
            "command" : UndoableCLICommand,
            "function" : UMLModel.rename_method,
            "num_arguments" : 3,
            "skip_line" : False
        }
    ],
    "delete_method" : [
        {
            "usage" : "delete_method <class_name> <method_name>",
            "desc" : "deletes the method from the class",
            "command" : UndoableCLICommand,
            "function" : UMLModel.delete_method,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],
    "move_up_method" : [
        {
            "usage" : "move_up_method <class_name> <method_name>",
            "desc" : "moves method up one space in a list of methods",
            "command" : UndoableCLICommand,
            "function" : UMLModel.move_up_method,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],
    "move_down_method" : [
        {
            "usage" : "move_down_method <class_name> <method_name>",
            "desc" : "moves method down one space in a list of methods",
            "command" : UndoableCLICommand,
            "function" : UMLModel.move_down_method,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],
    "list_methods" : [
        {
            "usage" : "list_methods <class_name>",
            "desc" : "prints all of the methods for a given class",
            "command" : CLICommand,
            "function" : UMLModel.list_methods,
            "num_arguments" : 1,
            "skip_line" : True
        }
    ],
    "create_parameter" : [
        {
            "usage" : "create_parameter <class_name> <method_name> <parameter_type> <parameter_name>",
            "desc" : "creates a parameter named <parameter_name> of type <parameter_type> and adds it to the given class and method\n ",
            "command" : UndoableCLICommand,
            "function" : UMLModel.create_parameter,
            "num_arguments" : 4,
            "skip_line" : False
        }
    ],
    "list_parameters" : [
        {
            "usage" : "list_parameters <class_name> <method_name>",
            "desc" : "lists all the paramters for <method_name> in <class_name>\n ",
            "command" : UndoableCLICommand,
            "function" : UMLModel.list_parameters,
            "num_arguments" : 2,
            "skip_line" : True
        }
    ],
    "create_relationship" : [
        {
            "usage" : "create_relationship <relationship_type> <class1> <class2>",
            "desc" : "creates a relationship between <class1> and <class2>\n<relationship_type> should be one of \n{inheritance, generalization, aggregation, composition}",
            "command" : UndoableCLICommand,
            "function" : UMLModel.create_relationship,
            "num_arguments" : 3,
            "skip_line" : False
        }
    ],
    "delete_relationship" : [
        {
            "usage" : "delete_relationship <class1> <class2>",
            "desc" : "removes the relationship between <class1> and <class2>",
            "command" : UndoableCLICommand,
            "function" : UMLModel.delete_relationship,
            "num_arguments" : 2,
            "skip_line" : False
        }
    ],
    "move_up_relationship" : [
       {
            "usage" : "move_up_relationship <class_name1> <class_name2>",
            "desc" : "moves relationship up one space in a list of the first specified class's relationships",
            "function" : UMLModel.move_up_relationship,
            "num_arguments" : 2,
            "skip_line" : False
       }
    ],
    "move_down_relationship" : [
       {
            "usage" : "move_down_relationship <class_name1> <class_name2>",
            "desc" : "moves relationship down one space in a list of the first specified class's relationships",
            "function" : UMLModel.move_down_relationship,
            "num_arguments" : 2,
            "skip_line" : False
       }
    ],
    "list_relationships" : [
        {
            "usage" : "list_relationships",
            "desc" : "prints out the classes that each class relate to",
            "command" : CLICommand,
            "function" : UMLModel.list_relationships,
            "num_arguments" : 0,
            "skip_line" : False
        },
        {
            "usage" : "list_relationships <class_name>",
            "desc" : "prints out the classes that a relate to class_name",
            "command" : CLICommand,
            "function" : UMLModel.list_relationships,
            "num_arguments" : 1,
            "skip_line" : True
        }
    ],
    "save_model" : [
        {
            "usage" : "save_model <filename>",
            "desc" : "saves the UMLModel into <filename> as JSON",
            "command" : CLICommand,
            "function" : UMLModel.save_model,
            "num_arguments" : 1,
            "skip_line" : False
        }
    ],
    "load_model" : [
        {
            "usage" : "load_model <filename>",
            "desc" : "loads the UMLModel from <filename> and uses it as the working UMLModel",
            "command" : CLICommand,
            "function" : UMLModel.load_model,
            "num_arguments" : 1,
            "skip_line" : True
        }
    ],
    "undo" : [
        {
            "usage" : "undo", 
            "desc" : "undoes the last undoable command (if there was one)",
            "command" : CLICommand,
            "function" : CLIEditor.undo,
            "num_arguments" : 0,
            "skip_line" : False
        }
    ],
    "redo" : [
        {
            "usage" : "redo", 
            "desc" : "redoes the last undo'd command (if there was one)",
            "command" : CLICommand,
            "function" : CLIEditor.redo,
            "num_arguments" : 0,
            "skip_line" : True
        }
    ],
    "help" : [
        {
            "usage" : "help", 
            "desc" : "lists all possible commands",
            "command" : CLICommand,
            "function" : CLIEditor.print_help_message,
            "num_arguments" : 0,
            "skip_line" : False
        },
        {
            "usage" : "help <command_name>", 
            "desc" : "lists the usage for <command_name>",
            "command" : CLICommand,
            "function" : CLIEditor.print_help_message,
            "num_arguments" : 1,
            "skip_line" : False
        }
    ],
    "exit" : [
        {
            "usage" : "exit",
            "desc" : "exits the program",
            "command" : CLICommand,
            "function" : CLIEditor.prompt_exit,
            "num_arguments" : 0,
            "skip_line" : False
        }
    ],
}