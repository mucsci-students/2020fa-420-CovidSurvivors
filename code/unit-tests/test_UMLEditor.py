# Unit test for the UMLEditor class
# Description:     
#   This file validates that the execute function belonging to the UMLEditor class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20, 2020

##########################################################################
# Imports

import unittest
import sys
sys.path.append('../')
from UMLEditor import UMLModel
import UMLEditor as editor


##########################################################################

model = UMLModel()

# Unit test for the UMLEditor

class TestUMLEditor(unittest.TestCase):

    # calls the REPL method
    def REPL(self):
        editor.REPL()

    # validates intended behavior of execute method
    def test_execute(self):
        # test help WITHOUT arguments
        print("-------------------------------")
        print("-------------------------------")
        print("Testing invalid commands.")
        print("Command: dog")
        editor.execute(model, "dog", [])
        print("-------------------------------")
        print("Testing help without arguments.")
        editor.execute(model, "help", [])

        # test help WITH arguments
        print("------------------------------")
        print("Testing help with arguments.")
        editor.execute(model, "help", ["create_class"])

        # test create_class
        print("------------------------------")
        print("Testing create_class.")
        editor.execute(model, "create_class", ["ClassA"])
        editor.execute(model, "create_class", ["ClassB"])
        editor.execute(model, "create_class", ["ClassC"])

        # check current list of classes
        # test list_classes
        print("-------------------------------")
        print("Testing list_classes.")
        print("Current list of classes:")
        editor.execute(model, "list_classes", [])

        # test rename_class
        print("-------------------------------")
        print("Testing rename_class.")
        editor.execute(model, "rename_class", ["ClassA", "ClassOne"])
        editor.execute(model, "rename_class", ["ClassB", "ClassTwo"])

        # test delete_class
        print("-------------------------------")
        print("Testing delete_class.")
        editor.execute(model, "delete_class", ["ClassC"])

        # check current list of classes
        print("Current list of classes:")
        editor.execute(model, "list_classes", [])

        # test create_attribute
        print("-------------------------------")
        print("Testing create_attribute.")
        editor.execute(model, "create_attribute", ["ClassOne", "foo"])
        editor.execute(model, "create_attribute", ["ClassOne", "John"])

        # test list_attributes
        print("-------------------------------")
        print("Testing list_attributes for ClassOne.")
        editor.execute(model, "list_attributes", ["ClassOne"])
        print("-------------------------------")
        print("Testing list_attributes for ClassTwo.")
        editor.execute(model, "list_attributes", ["ClassTwo"])

        # test rename_attribute
        print("-------------------------------")
        print("Testing rename_attribute.")
        editor.execute(model, "rename_attribute", ["ClassOne", "foo", "bar"])
        print("Current attribute list for ClassOne:")
        editor.execute(model, "list_attributes", ["ClassOne"])

        # test delete_attribute
        print("-------------------------------")
        print("Testing delete_attribute.")
        editor.execute(model, "delete_attribute", ["ClassOne", "John"])
        print("Current attribute list for ClassOne:")
        editor.execute(model, "list_attributes", ["ClassOne"])

        # test create_relationship
        print("-------------------------------")
        print("Testing create_relationship.")
        editor.execute(model, "create_relationship", ["pow", "ClassOne", "ClassTwo"])

        # test list_relationships WITHOUT arguments
        print("-------------------------------")
        print("Testing list_relationships without arguments.")
        print("Current list of relationships:")
        editor.execute(model, "list_relationships", [])

        #test list_relationships WITH arguments
        print("-------------------------------")
        print("Testing list_relationships with arguments.")
        editor.execute(model, "list_relationships", ["ClassOne"])

        # test delete relationships
        print("-------------------------------")
        print("Testing delete_relationship.")
        editor.execute(model, "delete_relationship", ["ClassOne", "ClassTwo"])
        editor.execute(model, "list_relationships", ["ClassOne"])

        # test save_editor
        print("-------------------------------")
        print("Testing save_editor")
        editor.execute(model, "save_model", [])

        # test exit
        print("-------------------------------")
        print("Testing exit")
        editor.execute(model, "exit", ["boo"])

        # restart REPL
        editor.REPL()

        # test load_editor
        print("-------------------------------")
        print("Testing save_editor")
        editor.execute(model, "load_model", ["boo"])

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLEditor.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLEditor.py' command
if __name__ == '__main__':
    unittest.main()

