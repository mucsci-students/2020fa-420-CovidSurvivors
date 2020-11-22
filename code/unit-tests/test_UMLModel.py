# Unit test for the UMLModel class
# Description:
#   This file validates that each function belonging to the UMLModel class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20, 2020

##########################################################################
# Imports

import unittest
import pytest
import sys
sys.path.append('../')
sys.path.append('code/')
from UMLEditor import main
from models.UMLModel import UMLModel
from models.UMLClass import UMLClass
import io

##########################################################################

# Unit test for the UMLModel

class UMLModelTest(unittest.TestCase):

    # validates intended behavior of create_class method
    def test_create_class(self):
        model = UMLModel()

        # Ensure class is created
        model.create_class("class1")
        self.assertEqual(model.classes["class1"].name, "class1")

        # Ensure duplicate class is not created
        status, msg = model.create_class("class1")
        self.assertFalse(status)
        self.assertEqual(msg, "class1 already exists.")

    ######################################################################

    # validates intended behavior of rename_class method
    def test_rename_class(self):
        model = UMLModel()
        model.create_class("class1")

        # Ensure name is changed
        model.rename_class("class1", "classA")
        # assert dictionary key was changed
        self.assertTrue("classA" in model.classes)
        #assert class object name was changed
        self.assertEqual(model.classes["classA"].name, "classA")

        # Ensure unknown class is rejected
        status, msg = model.rename_class("class1", "classB")
        self.assertFalse(status)
        self.assertEqual(msg, "class1 does not exist.")

        # Ensure duplicate newname is rejected
        model.create_class("class1")
        status, msg = model.rename_class("classA", "class1")
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "class1 already exists.")

        # Ensure renamed class with relationship updates
        # relationship in both classes
        self.assertTrue(model.create_class("class2")[0])
        self.assertTrue(model.create_relationship("inheritance", "class1", "class2")[0])
        self.assertTrue(model.rename_class("class2", "class3")[0])
        self.assertEqual(model.classes["class1"].relationships[0].other, "class3")

    ######################################################################

    # validates intended behavior of delete_class method
    def test_delete_class(self):
        model = UMLModel()
        model.create_class("class1")

        # Ensure deleted
        model.delete_class("class1")
        # assert dictionary key was removed
        self.assertTrue("class1" not in model.classes)

        # Ensure no errors when class DNE
        status, msg = model.delete_class("class1")
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "class1 does not exist.")

    ######################################################################

    # validates intended behavior of create_field method
    def test_create_field(self):
        model = UMLModel()
        model.create_class("class1")
        testClass = model.classes["class1"]

        # Ensure field is created
        model.create_field("class1", "public", "void", "a1")
        self.assertTrue(testClass.has_field("a1"))

        # Ensure duplicate field is not created
        status, msg = model.create_field("class1", "public", "void", "a1")
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "field a1 already exists in class1")

    ######################################################################

    # validates intended behavior of find_field method
    def test_find_field(self):
        model = UMLModel()
        model.create_class("class1")
        testClass = model.classes["class1"]

        # create some fields
        model.create_field("class1", "public", "void", "a1")
        model.create_field("class1", "private", "int", "num")

        # ensure fields are found in the right indices
        self.assertEqual(model.find_field("class1", "a1"), 0)
        self.assertEqual(model.find_field("class1", "num"), 1)

    ######################################################################

    # validates intended behavior of rename_field method
    def test_rename_field(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_field("class1", "public", "void", "a1")

        # Ensure field is renamed
        model.rename_field("class1", "a1", "a2")
        self.assertEqual(model.classes["class1"].fields[0].name, "a2")

    ######################################################################

    # validates intended behavior of delete_field method
    def test_delete_field(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_field("class1", "public", "void", "a1")
        testClass = model.classes["class1"]

        # Ensure field is deleted
        model.delete_field("class1", "a1")
        self.assertFalse(testClass.has_field("a1"))

    ######################################################################
    def test_move_up_field(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_field("class1", "public", "void", "a1")
        model.create_field("class1", "public", "void", "a2")
        model.create_field("class1", "public", "void", "a3")
        testClass = model.classes["class1"]

        # Ensure the field's were created
        self.assertTrue(testClass.has_field("a1"))  
        self.assertTrue(testClass.has_field("a2"))
        self.assertTrue(testClass.has_field("a3"))

        # Ensure the fields'position 
        self.assertEqual(testClass.field_index("a1"), 0)
        self.assertEqual(testClass.field_index("a2"), 1)
        self.assertEqual(testClass.field_index("a3"), 2)

        # Move up the field one position from the list
        model.move_up_field("class1", "a2") 
        
        # Ensure the field has a right position
        self.assertEqual(testClass.field_index("a2"), 0)
        self.assertEqual(testClass.field_index("a1"), 1)
        self.assertEqual(testClass.field_index("a3"), 2)
        
    ######################################################################
    # Moves a field up one position in a list of fields for a given class
    def test_move_down_field(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_field("class1", "public", "void", "a1")
        model.create_field("class1", "public", "void", "a2")
        model.create_field("class1", "public", "void", "a3")
        model.create_field("class1", "public", "void", "a4")
        # ensure the class is created
        testClass = model.classes["class1"]
        
        # Ensure the fields were created
        self.assertTrue(testClass.has_field("a1"))  
        self.assertTrue(testClass.has_field("a2"))
        self.assertTrue(testClass.has_field("a3"))
        self.assertTrue(testClass.has_field("a4"))
        
        # Ensure the fields'position  
        self.assertEqual(testClass.field_index("a1"), 0)
        self.assertEqual(testClass.field_index("a2"), 1)
        self.assertEqual(testClass.field_index("a3"), 2)
        self.assertEqual(testClass.field_index("a4"), 3)
        
        # Move down the field one position from the list
        model.move_down_field("class1", "a1") 
        
        # Ensure the field has a right position
        self.assertEqual(testClass.field_index("a2"), 0)
        self.assertEqual(testClass.field_index("a1"), 1)
        self.assertEqual(testClass.field_index("a3"), 2)
        self.assertEqual(testClass.field_index("a4"), 3)
        
    ######################################################################

    # validates intended behavior of create_method method
    def test_create_method(self):
        model = UMLModel()
        model.create_class("class1")
        testClass = model.classes["class1"]

        # Ensure method is created
        model.create_method("class1", "public", "void", "add")
        self.assertTrue(testClass.has_method("add"))

        # Ensure duplicate method is not created
        status, msg = model.create_method("class1", "public", "void", "add")
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "method add already exists in class1")

    ######################################################################

    # validates intended behavior of rename_mehod method
    def test_rename_method(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "void", "add")

        # Ensure method is renamed
        model.rename_method("class1", "add", "subtract")
        self.assertEqual(model.classes["class1"].methods[0].name, "subtract")

    ######################################################################

    # validates intended behavior of delete_method method
    def test_delete_method(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "void", "add")
        testClass = model.classes["class1"]

        # Ensure method is deleted
        model.delete_method("class1", "add")
        self.assertFalse(testClass.has_method("add"))

    ##########################################################################

    # validates intended behavior of create_parameter method
    def test_create_parameter(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "string", "method1")
        model.create_parameter("class1", "method1", "param_type", "param_name")

        self.assertTrue(model.classes["class1"].methods[model.classes["class1"].method_index("method1")].has_parameter("param_name"))


        # Ensure duplicate parameter is not created
        status, msg = model.create_parameter("class1", "method1", "param_type", "param_name")

        # ensure it failed
        self.assertFalse(status)

    ######################################################################

    # validates intended behavior of rename_parameter method
    def test_rename_parameter(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "string", "method1")
        model.create_parameter("class1", "method1", "param_type", "param_name")
        
        #ensure parameter is renamed
        model.rename_parameter("class1", "method1", "param_name", "new_param_name")
        
        # Ensure duplicate parameter is not created
        self.assertEqual(model.classes["class1"].methods[model.classes["class1"].method_index("method1")].parameters[0].name, "new_param_name")

    ######################################################################

    # validates intended behavior of delete_parameter method
    def test_delete_parameter(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "string", "method1")
        model.create_parameter("class1", "method1", "param_type", "param_name")
        testClass = model.classes["class1"]
        
        #ensure parameter is deleted
        model.delete_parameter("class1", "method1", "parameter_name")
        self.assertFalse(testClass.methods[testClass.method_index("method1")].has_parameter("parameter_name"))

    ######################################################################

    # validates intended behavior of create_relationship method
    def test_create_relationship(self):
        model = UMLModel()
        model.create_class("c1")
        model.create_class("c2")

        # Ensure relationship is created
        model.create_relationship("composition", "c1", "c2")
        self.assertTrue(model.classes["c1"].has_relationship("c2"))
        self.assertTrue(model.classes["c2"].has_relationship("c1"))

        # Ensure already existing rel
        status, msg = model.create_relationship("composition","c2","c1")
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "Relationship between 'c2' and 'c1' already exists.")

    ######################################################################

    # validates intended behavior of delete_relationship method
    def test_delete_relationship(self):
        model = UMLModel()
        model.create_class("c1")
        model.create_class("c2")
        model.create_relationship("r1", "c1", "c2")

        # Ensure relationship is created
        model.delete_relationship("c1","c2")
        self.assertEqual(len(model.classes["c1"].relationships), 0)
        self.assertEqual(len(model.classes["c2"].relationships), 0)

    ######################################################################

# runs all of our tests
# allows us to run this file using the typical 'python3 test_UMLModel.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLModel.py' command
if __name__ == '__main__':
    unittest.main()
