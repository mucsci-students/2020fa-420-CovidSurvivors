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
import CLI.CLIEditor as editor
from CLI.CLIEditor import UMLModel


##########################################################################

model = UMLModel()

def separate():
    print("-----------------------------------------------------------------------------------------------")

# Unit test for the UMLEditor

class TestUMLEditor(unittest.TestCase):

    # calls the REPL method
    def REPL(self):
        editor.REPL()

    # validates intended behavior of execute method
    def test_execute(self):
        # test help WITHOUT arguments
        separate()
        separate()
        print("Testing invalid commands.")
        print("Command: dog")
        editor.execute(model, "dog", [])
        separate()
        print("Testing help without arguments.")
        editor.execute(model, "help", [])

        # test help WITH arguments
        separate()
        print("Testing help with arguments.")
        editor.execute(model, "help", ["create_class"])

        # test create_class
        separate()
        print("Testing create_class.")
        editor.execute(model, "create_class", ["ClassA"])
        editor.execute(model, "create_class", ["ClassB"])
        editor.execute(model, "create_class", ["ClassC"])

        # check current list of classes
        # test list_classes
        separate()
        print("Testing list_classes.")
        print("Current list of classes:")
        editor.execute(model, "list_classes", [])

        # test rename_class
        separate()
        print("Testing rename_class.")
        editor.execute(model, "rename_class", ["ClassA", "ClassOne"])
        editor.execute(model, "rename_class", ["ClassB", "ClassTwo"])
        print("Current list of classes:")
        editor.execute(model, "list_classes", [])

        # test delete_class
        separate()
        print("Testing delete_class.")
        editor.execute(model, "delete_class", ["ClassC"])

        # check current list of classes
        print("Current list of classes:")
        editor.execute(model, "list_classes", [])

        # test create_field
        separate()
        print("Testing create_field.")
        editor.execute(model, "create_field", ["ClassOne", "public", "int", "foo"])
        editor.execute(model, "create_field", ["ClassOne", "private", "string", "John"])

        # test list_fields
        separate()
        print("Testing list_fields for ClassOne.")
        editor.execute(model, "list_fields", ["ClassOne"])
        separate()
        print("Testing list_fields for ClassTwo.")
        editor.execute(model, "list_fields", ["ClassTwo"])

        # test rename_field
        separate()
        print("Testing rename_field.")
        editor.execute(model, "rename_field", ["ClassOne", "foo", "bar"])
        print("Current field list for ClassOne:")
        editor.execute(model, "list_fields", ["ClassOne"])

        # test delete_field
        separate()
        print("Testing delete_field.")
        editor.execute(model, "delete_field", ["ClassOne", "John"])
        print("Current field list for ClassOne:")
        editor.execute(model, "list_fields", ["ClassOne"])

        # test create_method
        separate()
        print("Testing create_method.")
        editor.execute(model, "create_method", ["ClassOne", "public", "void", "concatenate()"])
        editor.execute(model, "create_method", ["ClassOne", "private", "string", "getLastName()"])
        editor.execute(model, "create_method", ["ClassOne", "public", "int", "add()"])
        editor.execute(model, "create_method", ["ClassTwo", "private", "char", "getInitial()"])
        editor.execute(model, "create_method", ["ClassTwo", "public", "double", "getSalary()"])
        editor.execute(model, "create_method", ["ClassTwo", "private", "string", "getSSN()"])

        # test list_methods
        separate()
        print("Testing list_methods for ClassOne.")
        editor.execute(model, "list_methods", ["ClassOne"])
        separate()
        print("Testing list_methods for ClassTwo.")
        editor.execute(model, "list_methods", ["ClassTwo"])

        # test rename_field
        separate()
        print("Testing rename_method.")
        editor.execute(model, "rename_method", ["ClassOne", "concatenate()", "delete()"])
        print("Current method list for ClassOne:")
        editor.execute(model, "list_methods", ["ClassOne"])

        # test delete_method
        separate()
        print("Testing delete_method.")
        editor.execute(model, "delete_method", ["ClassTwo", "getSSN()"])
        print("Current method list for ClassTwo:")
        editor.execute(model, "list_methods", ["ClassTwo"])        

        # test create_relationship
        separate()
        print("Testing create_relationship.")
        editor.execute(model, "create_relationship", ["inheritance", "ClassOne", "ClassTwo"])

        # test list_relationships WITHOUT arguments
        separate()
        print("Testing list_relationships without arguments.")
        print("Current list of relationships:")
        editor.execute(model, "list_relationships", [])

        #test list_relationships WITH arguments
        separate()
        print("Testing list_relationships with arguments.")
        editor.execute(model, "list_relationships", ["ClassOne"])
        
        #test list_class
        separate()
        print("Testing list_class.")
        editor.execute(model, "list_class", ["ClassOne"])
        editor.execute(model, "list_class", ["ClassTwo"])

        # test delete relationship
        separate()
        print("Testing delete_relationship.")
        editor.execute(model, "delete_relationship", ["ClassOne", "ClassTwo"])
        editor.execute(model, "list_relationships", ["ClassOne"])

##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLEditor.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLEditor.py' command
if __name__ == '__main__':
    unittest.main()

