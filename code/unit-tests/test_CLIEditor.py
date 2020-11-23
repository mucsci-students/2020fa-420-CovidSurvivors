# Unit test for the CLIEditor
# Description:
#   This file validates that each function belonging to the CLIEditor
#   class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     November 21, 2020

##########################################################################
# Imports

import unittest
import pytest
import sys
sys.path.append('../')
sys.path.append('code/')
from CLI.CLIEditor import *
from models.UMLModel import UMLModel
from command.command import CommandHistory
import io

##########################################################################

# Unit tests for CLIEditor functions
class TestCLI(unittest.TestCase):

    # ensures executeCMD works properly 
    def test_executeCMD(self):
        model = UMLModel()
        command_history = CommandHistory(HISTORY_LIMIT)

        # Test1 : simple cmd 
        executeCMD(model, command_history, "create_class", ["class1"]) 
        # ensure model has the new class
        self.assertTrue("class1" in model.classes)
        # ensure command is in history
        self.assertTrue(len(command_history.history) == 1)

        # Test2 : invalid cmd 
        captured = io.StringIO()
        sys.stdout = captured
        executeCMD(model, command_history, "not_a_command", [])
        # ensure error message was given
        self.assertEqual(captured.getvalue(), f"{ERROR_COLOR}CommandError:{NORMAL_COLOR} "
            f"'not_a_command' is not a valid command\ntype 'help' for a list of valid commands\n")

        # Test3 : invalid length of arguments
        captured = io.StringIO()
        sys.stdout = captured
        commandName = "create_field"
        executeCMD(model, command_history, commandName, ["name"])
        # ensure error message was given
        self.assertEqual(captured.getvalue(), f"{ERROR_COLOR}CommandError:{NORMAL_COLOR} "
            f"Incorrect usage of {commandName}\ntype 'help {commandName}' to see valid usages of {commandName}\n")

        # Test4 : valid cmd with arguments that fail
        captured = io.StringIO()
        sys.stdout = captured
        executeCMD(model, command_history, "create_class", ["class1"])
        # ensure error message was given
        self.assertTrue(captured.getvalue().startswith(f"{ERROR_COLOR}ERROR:{NORMAL_COLOR}"))

        # Test5 : non-undoable command
        captured = io.StringIO()
        sys.stdout = captured
        command_history = CommandHistory(HISTORY_LIMIT)
        executeCMD(model, command_history, "list_classes", [])
        # ensure success
        self.assertTrue(captured.getvalue().startswith(f"{SUCCESS_COLOR}SUCCESS:{NORMAL_COLOR}"))
        # ensure command was not added to history
        self.assertEqual(len(command_history.history), 0)
    
    # ensures fetch_classes works properly
    def test_fetch_classes(self):

        model = UMLModel()

        # Test 1: no classes
        classes = fetch_classes(model)
        self.assertEqual(classes, [])

        # Test 2: multiple classes
        model.create_class("class1")
        model.create_class("class2")
        model.create_class("class3")
        classes = fetch_classes(model)
        self.assertTrue("class1" in classes)
        self.assertTrue("class2" in classes)
        self.assertTrue("class3" in classes)

    # ensures fetch_from_class works properly
    def test_fetch_from_class(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_class("class2")
        model.create_field("class1", "public", "string", "field1")
        model.create_field("class1", "public", "int", "field2")
        model.create_method("class1", "public", "int", "method1")
        model.create_method("class1", "public", "bool", "method2")
        model.create_relationship("inheritance", "class1", "class2")

        # Test 1: fetch fields
        fields = fetch_from_class(model, "class1", "fields")
        self.assertEqual(fields, ["field1", "field2"])

        # Test 2: fetch methods
        methods = fetch_from_class(model, "class1", "methods")
        self.assertEqual(methods, ["method1", "method2"])

        # Test 3: empty list
        fields = fetch_from_class(model, "class2", "fields")
        self.assertEqual(fields, [])

    # ensures fetch_from_method works properly
    def test_fetch_from_method(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "int", "method1")
        model.create_parameter("class1", "method1", "int", "num")
        model.create_parameter("class1", "method1", "bool", "isTrue")
        model.create_method("class1", "public", "bool", "method2")

        # Test 1: get parameters 
        params = fetch_from_method(model, "class1", "method1")
        self.assertEqual(params, ["num", "isTrue"])

        # Test 2: no parameters
        params = fetch_from_method(model, "class1", "method2")
        self.assertEqual(params, [])

    # ensures print_help_message works properly
    def test_print_help_message(self):
        # Test 1: without command
        captured = io.StringIO()
        sys.stdout = captured
        print_help_message(UMLModel())
        self.assertEqual(captured.getvalue(), "Type help <command_name> to see the usage of a command\n"
            "\t create_class\n"
            "\t rename_class\n"
            "\t delete_class\n"
            "\t list_class\n"
            "\t list_classes\n"
            "\n"
            "\t create_field\n"
            "\t rename_field\n"
            "\t delete_field\n"
            "\t move_up_field\n"
            "\t move_down_field\n"
            "\t list_fields\n"
            "\n"
            "\t create_method\n"
            "\t rename_method\n"
            "\t delete_method\n"
            "\t move_up_method\n"
            "\t move_down_method\n"
            "\t list_methods\n"
            "\n"
            "\t create_parameter\n"
            "\t rename_parameter\n"
            "\t delete_parameter\n"
            "\t list_parameters\n"
            "\n"
            "\t create_relationship\n"
            "\t delete_relationship\n"
            "\t move_up_relationship\n"
            "\t move_down_relationship\n"
            "\t list_relationships\n"
            "\n"
            "\t save_model\n"
            "\t load_model\n"
            "\n"
            "\t undo\n"
            "\t redo\n"
            "\n"
            "\t help\n"
            "\t exit\n"
)
        
        # Test 2: with valid command name
        captured = io.StringIO()
        sys.stdout = captured
        print_help_message(UMLModel(), "create_class")
        self.assertEqual(captured.getvalue(), "Usage:\n"
            f"  {DESCRIPTION_COLOR}create_class <class_name>{NORMAL_COLOR}\n"
            "Description:\n"
            "  creates a class named <class_name> and adds it to the model\n"
            )


        # Test 3: with invalid command name
        captured = io.StringIO()
        sys.stdout = captured
        print_help_message(UMLModel(), "not_a_command")
        self.assertEqual(captured.getvalue(), f"{ERROR_COLOR}ArgumentError:{NORMAL_COLOR} "
                f"'not_a_command' is not a valid command\n")


    # ensure prompt_exit works correctly
    def test_prompt_exit(self):

        # Test 1: fully exit 
        exits = False
        try:
            # give 'no' response for prompt_exit to grab and exit
            sys.stdin = io.StringIO("no\n")
            prompt_exit(UMLModel())
        except SystemExit:
            exits = True
        # make sure it exited
        self.assertTrue(exits)

        # Test 2: cancel exit 
        exits = False
        try:
            # give 'cancel' response for prompt_exit 
            sys.stdin = io.StringIO("cancel\n")
            status, msg = prompt_exit(UMLModel())
        except SystemExit:
            exits = True
        # make sure it didnt exit
        self.assertFalse(exits)
        self.assertEqual(msg, "Exit aborted")

        # Test 3: save model
        model1 = UMLModel()
        model1.create_class("class1")
        model1.create_class("class2")
        exits = False
        captured = io.StringIO()
        try:
            # give 'yes' response for prompt_exit to grab and exit
            sys.stdin = io.StringIO("yes\ntest_prompt_exit.json\n")
            prompt_exit(model1, os.getcwd() + "/code/data/")
        except SystemExit:
            exits = True
        # make sure it exited
        self.assertTrue(exits)
        # make sure it saved
        model2 = UMLModel()
        model2.load_model("test_prompt_exit.json", os.getcwd() + "/code/data/")
        self.assertEqual(model1.classes.keys(), model2.classes.keys())

    # ensure undo works properly
    def test_undo(self):
        model = UMLModel()
        command_history = CommandHistory(HISTORY_LIMIT)
        executeCMD(model, command_history, "create_class", ["class1"])
        # ensure class was there previously
        self.assertTrue("class1" in model.classes)

        # Test 1: undo valid command
        undo(command_history, [])
        # ensure command was undone
        self.assertTrue(len(model.classes) == 0)
        self.assertTrue(len(command_history.history) == 0)
        self.assertTrue(len(command_history.future) == 1)

        # Test 2: nothing to undo
        captured = io.StringIO()
        sys.stdout = captured
        undo(command_history, [])
        self.assertEqual(captured.getvalue(), f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} no command to undo\n")

    # ensure redo works properly
    def test_redo(self):
        model = UMLModel()
        command_history = CommandHistory(HISTORY_LIMIT)
        executeCMD(model, command_history, "create_class", ["class1"])
        # ensure class was there previously
        self.assertTrue("class1" in model.classes)
        undo(command_history, [])


        # Test 1: redo valid command
        redo(command_history, [])
        # ensure command was redone
        self.assertTrue("class1" in model.classes)
        self.assertTrue(len(command_history.history) == 1)
        self.assertTrue(len(command_history.future) == 0)

        # Test 2: nothing to redo
        captured = io.StringIO()
        sys.stdout = captured
        redo(command_history, [])
        self.assertEqual(captured.getvalue(), f"{ERROR_COLOR}ERROR:{NORMAL_COLOR} no command to redo\n")


# Unit test for REPL
class TestREPL(unittest.TestCase):

    # test only a couple do_*()
    def test_do_create_class(self):
        model = UMLModel()
        command_history = CommandHistory(HISTORY_LIMIT)
        repl = REPL(model, command_history)

        repl.do_create_class("class1")
        # ensure class was created
        self.assertTrue("class1" in model.classes)

    def test_do_create_field(self):
        model = UMLModel()
        model.create_class("class1")
        command_history = CommandHistory(HISTORY_LIMIT)
        repl = REPL(model, command_history)

        repl.do_create_field("class1 private int age")
        # ensure field was created
        self.assertTrue(model.classes["class1"].field_index("age") != -1)

    # test a couple complete_* functions
    def test_complete_rename_class(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_class("myclass")
        repl = REPL(model, CommandHistory(HISTORY_LIMIT))

        # Test 1: Tab before classname
        classnames = repl.complete_rename_class("", "rename_class ", 0, 0)
        self.assertEqual(classnames, ["class1", "myclass"])

        # Test 2: Tab in the middle of classname - only one match
        classnames = repl.complete_rename_class("cl", "rename_class cl", 0, 0)
        self.assertEqual(classnames, ["class1"])

        # Test 3: Tab after classname
        classnames = repl.complete_rename_class("class1", "rename_class class1", 0, 0)
        self.assertEqual(classnames, ["class1"])

        # Test 4: Tab before second classname
        classnames = repl.complete_rename_class("", "rename_class class1 ", 0, 0)
        self.assertEqual(classnames, [])

        # Test 5: Tab after second classname
        classnames = repl.complete_rename_class("newclassname", "rename_class class1 newclassname", 0, 0)
        self.assertEqual(classnames, [])

    def test_complete_delete_class(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_class("myclass")
        repl = REPL(model, CommandHistory(HISTORY_LIMIT))

        # Test 1: Tab before classname
        classnames = repl.complete_delete_class("", "delete_class ", 0, 0)
        self.assertEqual(classnames, ["class1", "myclass"])

        # Test 2: Tab in the middle of classname - only one match
        classnames = repl.complete_delete_class("cl", "delete_class cl", 0, 0)
        self.assertEqual(classnames, ["class1"])

        # Test 3: Tab after classname
        classnames = repl.complete_delete_class("", "delete_class class1 ", 0, 0)
        self.assertEqual(classnames, [])


    def test_complete_rename_parameter(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "int", "method1")
        model.create_parameter("class1", "method1", "int", "a")
        model.create_parameter("class1", "method1", "int", "b")
        model.create_parameter("class1", "method1", "int", "abba")
        model.create_method("class1", "public", "int", "method2")
        model.create_method("class1", "public", "int", "mymethod")
        model.create_class("myclass")
        repl = REPL(model, CommandHistory(HISTORY_LIMIT))

        # Test 1: Tab before classname
        classnames = repl.complete_rename_parameter("", "rename_parameter ", 0, 0)
        self.assertEqual(classnames, ["class1", "myclass"])

        # Test 2: Tab in the middle of classname - only one match
        classnames = repl.complete_rename_parameter("cl", "rename_parameter cl", 0, 0)
        self.assertEqual(classnames, ["class1"])

        # Test 3: Tab before methodname
        classnames = repl.complete_rename_parameter("", "rename_parameter class1 ", 0, 0)
        self.assertEqual(classnames, ["method1", "method2", "mymethod"])

        # Test 4: Tab during methodname
        classnames = repl.complete_rename_parameter("met", "rename_parameter class1 met", 0, 0)
        self.assertEqual(classnames, ["method1", "method2"])

        # Test 5: Tab before old param name
        classnames = repl.complete_rename_parameter("", "rename_parameter class1 method1 ", 0, 0)
        self.assertEqual(classnames, ["a", "b", "abba"])

        # Test 6: Tab during old param name
        classnames = repl.complete_rename_parameter("a", "rename_parameter class1 method1 a", 0, 0)
        self.assertEqual(classnames, ["a","abba"])

        # Test 7: Tab after old param name 
        classnames = repl.complete_rename_parameter("", "rename_parameter class1 method1 abba ", 0, 0)
        self.assertEqual(classnames, [])

        # Test 8: Tab after old param name 
        classnames = repl.complete_rename_parameter("iLikePie", "rename_parameter class1 method1 abba iLikePie", 0, 0)
        self.assertEqual(classnames, [])