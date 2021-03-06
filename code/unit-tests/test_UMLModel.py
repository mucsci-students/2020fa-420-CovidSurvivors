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
import json
import os
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
        model.create_class("class2")

        # create relationship between classes
        model.create_relationship("composition", "class1", "class2")
        # Ensure relationship is created
        self.assertTrue(model.classes["class1"].has_relationship("class2"))
        self.assertTrue(model.classes["class2"].has_relationship("class1"))

        # Ensure deleted
        model.delete_class("class1")
        # assert dictionary key was removed
        self.assertTrue("class1" not in model.classes)

        # Ensure relationship was removed after deletion of class1
        status, msg = model.list_relationships("class2")
        self.assertTrue(status)
        self.assertEqual(msg, "Class 'class2' has no relationships")
        
        # Ensure no errors when class DNE
        status, msg = model.delete_class("class1")
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "class1 does not exist.")
        
    ######################################################################

    # validates intended behavior of list_class method
    def test_list_class(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_class("class2")
        model.create_class("class3")

        # variables used for testing equality
        message = model.list_class("class5")[1]
        # test output equality while using the wrong class name
        self.assertEqual(message, "'class5' is not a valid class")
        
        # add fields to class1
        model.create_field("class1", "public", "void", "a1")
        model.create_field("class1", "private", "int", "size")
        # add methods to class1 along with some parameters
        model.create_method("class1", "protected", "void", "setSpeed")
        model.create_method("class1", "public", "void", "walk")
        model.create_parameter("class1", "setSpeed", "int", "speed")
        model.create_parameter("class1", "walk", "int", "speed")
        model.create_parameter("class1", "walk", "double", "direction")
        # add relationships to class1
        model.create_relationship("inheritance", "class1", "class2")
        model.create_relationship("aggregation", "class3", "class1")

        # variables used for testing equality
        message = model.list_class("class1")[1]
        outString = "".join(("Class: class1\n", 
                    "=== Fields ======================\n", 
                    "public a1: void\n", 
                    "private size: int\n", 
                    "=== Methods =====================\n", 
                    "protected setSpeed(int speed): void\n", 
                    "public walk(int speed, double direction): void\n", 
                    "=== Relationships ===============\n", 
                    "class1 ---------> class2\n", 
                    "class1 <<>>------ class3\n", 
                    "================================="))
        # test output equality            
        self.assertEqual(message,outString)
        
    ######################################################################

    # validates intended behavior of list_classes method
    def test_list_classes(self):
        model = UMLModel()

        # variables used for testing equality
        message = model.list_classes()[1]
        # test output equality without creating classes
        self.assertEqual(message, "No classes in the model")

        # create some classes
        model.create_class("class1")
        model.create_class("class2")
        model.create_class("class3")

        # variables used for testing equality
        message = model.list_classes()[1]
        outString = "".join(("Listing all classes in the model\n",
                            "class1\n", 
                            "class2\n", 
                            "class3"))
        # test output equality            
        self.assertEqual(message,outString)

    ######################################################################
    
    #validates intended behavior of set_class_position method
    def test_set_class_position(self):
        model = UMLModel()
        model.create_class("class1")
        
        # variables used for testing equality
        message = model.set_class_position("class3", 10, 20, 30)[1]
        # test output equality when class3 is a non-existent class
        self.assertEqual(message, "class3 does not exist")

        # set position of c1
        message = model.set_class_position("class1", 10, 20, 0)[1]
        # test output equality
        self.assertEqual(message, "The position of 'class1' has been set to ('10', '20')")

    ######################################################################

    # validates intended behavior of create_field method
    def test_create_field(self):
        model = UMLModel()
        model.create_class("class1")
        testClass = model.classes["class1"]

        # Ensure field is created
        model.create_field("class1", "public", "void", "a1")
        self.assertTrue(testClass.has_field("a1"))

        # Ensure we get correct output when class does not exist
        status, msg = model.create_field("class5", "private", "void", "a1")
        self.assertFalse(status)
        self.assertEqual(msg, "class5 does not exist")
      
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

        # ensure we get correct output when field is not found
        self.assertEqual(model.find_field("class1", "nonexistent"), -1)

    ######################################################################

    # validates intended behavior of rename_field method
    def test_rename_field(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_field("class1", "public", "void", "a1")

        # Ensure field is renamed
        model.rename_field("class1", "a1", "a2")
        self.assertEqual(model.classes["class1"].fields[0].name, "a2")

        # Ensure we get correct output when class doesn't exist
        status, msg = model.rename_field("class7", "a1", "a2")
        self.assertFalse(status)
        self.assertEqual(msg, "class7 does not exist.")

        # Ensure we get correct output when the field we wish to rename doesn't exist
        status, msg = model.rename_field("class1", "a7", "a3")
        self.assertFalse(status)
        self.assertEqual(msg, "field a7 does not exist in class1")

        # Ensure we get correct output when the new field already exist
        status, msg = model.rename_field("class1", "a2", "a2")
        self.assertFalse(status)
        self.assertEqual(msg, "field a2 already exists in class1")

    ######################################################################

    # validates intended behavior of delete_field method
    def test_delete_field(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_field("class1", "public", "void", "a1")
        testClass = model.classes["class1"]

        # Ensure we get correct output when class doesn't exist
        status, msg = model.delete_field("class5", "a1")
        self.assertFalse(status)
        self.assertEqual(msg, "class5 does not exist")

        # Ensure we get correct output when field we wish to remove doesn't exist
        status, msg = model.delete_field("class1", "a3")
        self.assertFalse(status)
        self.assertEqual(msg, "a3 is not a field of class1")

        # Ensure field is deleted
        model.delete_field("class1", "a1")
        self.assertFalse(testClass.has_field("a1"))

    ######################################################################
    
    # Moves a field up one position on a list of fields for a given class
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
        self.assertEqual(testClass.fields[0].name, "a1")
        self.assertEqual(testClass.fields[1].name, "a2")
        self.assertEqual(testClass.fields[2].name, "a3")
       
        # Move up the field one position from the list
        model.move_up_field("class1", "a2") 

        # Ensure the field has a right position
        self.assertEqual(testClass.field_index("a2"), 0)
        self.assertEqual(testClass.field_index("a1"), 1)
        self.assertEqual(testClass.field_index("a3"), 2)

        # Ensure the method don't move up any further
        status, msg = model.move_up_field("class1", "a2")
        self.assertFalse(status)
        self.assertEqual(msg, "a2 can not move up any further in class1")

        # Ensure correct response is outputted when class doesn't exist
        status, msg = model.move_up_field("class8", "a2")
        self.assertFalse(status)
        self.assertEqual(msg, "class8 does not exist")
        
        # Ensure correct response is outputted when field doesn't exist
        status, msg = model.move_up_field("class1", "a7")
        self.assertFalse(status)
        self.assertEqual(msg, "a7 does not exist in class1")
        
    ######################################################################
    
    # Moves a field one position down on the list of fields for a given class
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
        self.assertEqual(testClass.fields[0].name, "a1")
        self.assertEqual(testClass.fields[1].name, "a2")
        self.assertEqual(testClass.fields[2].name, "a3")
        self.assertEqual(testClass.fields[3].name, "a4")
        
        # Move down the field one position from the list
        model.move_down_field("class1", "a1") 
        
        # Ensure the field has a right position
        self.assertEqual(testClass.field_index("a2"), 0)
        self.assertEqual(testClass.field_index("a1"), 1)
        self.assertEqual(testClass.field_index("a3"), 2)
        self.assertEqual(testClass.field_index("a4"), 3)

        # Ensure the method don't move down further
        status, msg = model.move_down_field("class1", "a4")
        self.assertFalse(status)
        self.assertEqual(msg, "a4 can not move down any further in class1")

        # Ensure correct response is outputted when class doesn't exist
        status, msg = model.move_down_field("class8", "a4")
        self.assertFalse(status)
        self.assertEqual(msg, "class8 does not exist")
        
        # Ensure correct response is outputted when field doesn't exist
        status, msg = model.move_down_field("class1", "a7")
        self.assertFalse(status)
        self.assertEqual(msg, "a7 does not exist in class1")
        
    ######################################################################

    # validates intended behavior of list_fields method
    def test_list_fields(self):
        model = UMLModel()
        model.create_class("class1")

        # variables used for testing equality
        message = model.list_fields("class3")[1]
        # test output equality with a non-existent class
        self.assertEqual(message, "class3 is not a class")

        # variables used for testing equality
        message = model.list_fields("class1")[1]
        # test output equality without inserting fields
        self.assertEqual(message, "Class 'class1' has no fields")

        # add some fields to class1
        model.create_field("class1", "public", "int", "year")
        model.create_field("class1", "private", "int", "salary")
        model.create_field("class1", "protected", "string", "SSN")

        # variables used for testing equality
        message = model.list_fields("class1")[1]
        outString = "".join(("Fields of class1\n",
                            "PUBLIC int year\n", 
                            "PRIVATE int salary\n", 
                            "PROTECTED string SSN"))
        # test output equality            
        self.assertEqual(message,outString)
        
    ######################################################################

    # validates intended behavior of create_method method
    def test_create_method(self):
        model = UMLModel()
        model.create_class("class1")
        testClass = model.classes["class1"]

        # Ensure method is created
        model.create_method("class1", "public", "void", "add")
        self.assertTrue(testClass.has_method("add"))

        # Ensure we get correct output when class doesn't exist
        status, msg = model.create_method("class3", "public", "void", "subtract")
        self.assertFalse(status)
        self.assertEqual(msg, "class3 does not exist")

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

        # Ensure we get correct output when class doesn't exist
        status, msg = model.rename_method("class3", "add", "subtract")
        self.assertFalse(status)
        self.assertEqual(msg, "class3 does not exist")

        # Ensure we get correct output when method doesn't exist
        status, msg = model.rename_method("class1", "multiply", "subtract")
        self.assertFalse(status)
        self.assertEqual(msg, "method multiply does not exist in class1")

        # Ensure we get correct output when new method name already exists
        status, msg = model.rename_method("class1", "add", "add")
        self.assertFalse(status)
        self.assertEqual(msg, "method 'add' already exists in 'class1'")

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

        # Ensure we get correct output when class doesn't exist
        status, msg = model.delete_method("class4", "add")
        self.assertFalse(status)
        self.assertEqual(msg, "'class4' does not exist")

        # Ensure we get correct output when the method we wish to delete doesn't exist
        status, msg = model.delete_method("class1", "subtract")
        self.assertFalse(status)
        self.assertEqual(msg, "'subtract' does not exist in 'class1'")

        # Ensure method is deleted
        model.delete_method("class1", "add")
        self.assertFalse(testClass.has_method("add"))

   ######################################################################

    # validates intended behavior of list_methods method
    def test_list_methods(self):
        model = UMLModel()
        model.create_class("class1")

        # variables used for testing equality
        message = model.list_methods("class3")[1]
        # test output equality with a non-existent class
        self.assertEqual(message, "class3 does not exist")
        
        # variables used for testing equality
        message = model.list_methods("class1")[1]
        # test output equality without inserting methods 
        self.assertEqual(message, "class1 has no methods")

        # add some methods to class1
        model.create_method("class1", "public", "int", "getYear")
        model.create_method("class1", "private", "int", "getSalary")
        model.create_method("class1", "protected", "string", "getSSN")

        # variables used for testing equality
        message = model.list_methods("class1")[1]
        outString = "".join(("Methods for class1\n",
                            "PUBLIC getYear() : int\n", 
                            "PRIVATE getSalary() : int\n", 
                            "PROTECTED getSSN() : string"))
        # test output equality            
        self.assertEqual(message,outString) 
        
    ##########################################################################
    # Validates intended behavior of move_up_method
    def test_move_up_method(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "string", "method1")
        model.create_method("class1", "public", "string", "method2")
        model.create_method("class1", "public", "string", "method3")
        testClass = model.classes["class1"]

        # Ensure the methods were created in order position 
        self.assertEqual(testClass.methods[0].name, "method1")
        self.assertEqual(testClass.methods[1].name, "method2")
        self.assertEqual(testClass.methods[2].name, "method3")

        # Move up the method one position from the list
        model.move_up_method("class1", "method2")
        # Ensure the method has a right position after moved
        self.assertEqual(testClass.method_index("method2"), 0)
        self.assertEqual(testClass.method_index("method1"), 1)
        self.assertEqual(testClass.method_index("method3"), 2)

        # Ensure the method don't moove up further
        status, msg = model.move_up_method("class1", "method2")
        self.assertFalse(status)

        # Ensure correct response is outputted when class 1 doesn't exist
        status, msg = model.move_up_method("class7", "method2")
        self.assertFalse(status)
        self.assertEqual(msg, "class7 does not exist")
        
        # Ensure correct response is outputted when method doesn't exist
        status, msg = model.move_up_method("class1", "method9")
        self.assertFalse(status)
        self.assertEqual(msg, "method9 does not exist in class1")

    ######################################################################
    # Validates intended behavior of move_down_method
    def test_move_down_method(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "string", "method1")
        model.create_method("class1", "public", "string", "method2")
        model.create_method("class1", "public", "string", "method3")
        testClass = model.classes["class1"]

        # Ensure the methods'position 
        self.assertEqual(testClass.methods[0].name, "method1")
        self.assertEqual(testClass.methods[1].name, "method2")
        self.assertEqual(testClass.methods[2].name, "method3")

        # Move down the method one position from the list
        model.move_down_method("class1", "method2") 
        
        # Ensure the method has a right position after moved
        self.assertEqual(testClass.method_index("method1"), 0)
        self.assertEqual(testClass.method_index("method3"), 1)
        self.assertEqual(testClass.method_index("method2"), 2)
        
        # Ensure the method don't move down further
        status, msg = model.move_down_method("class1", "method2")
        self.assertFalse(status)

        # Ensure correct response is outputted when class doesn't exist
        status, msg = model.move_down_method("class7", "method2")
        self.assertFalse(status)
        self.assertEqual(msg, "class7 does not exist")
        
        # Ensure correct response is outputted when method doesn't exist
        status, msg = model.move_down_method("class1", "method9")
        self.assertFalse(status)
        self.assertEqual(msg, "method9 does not exist in class1")

    ######################################################################

    # validates intended behavior of create_parameter method
    def test_create_parameter(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_method("class1", "public", "string", "method1")
        model.create_parameter("class1", "method1", "param_type", "param_name")

        self.assertTrue(model.classes["class1"].methods[model.classes["class1"].method_index("method1")].has_parameter("param_name"))

        # Ensure we get correct output when class doesn't exist
        status, msg = model.create_parameter("class9", "method1", "param_type", "param_name")
        self.assertFalse(status)
        self.assertEqual(msg, "class9 does not exist")

        # Ensure we get correct output when method doesn't exist
        status, msg = model.create_parameter("class1", "method3", "param_type", "param_name")
        self.assertFalse(status)
        self.assertEqual(msg, "method method3 does not exist in class1")

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

        # Ensure we get correct output when class doesn't exist
        status, msg = model.rename_parameter("class9", "method1", "param_name", "new_param_name")
        self.assertFalse(status)
        self.assertEqual(msg, "class9 does not exist")

        # Ensure we get correct output when method doesn't exist
        status, msg = model.rename_parameter("class1", "method3", "param_name", "new_param_name")
        self.assertFalse(status)
        self.assertEqual(msg, "class1 does not have method, method3")

        # Ensure we get correct output when the parameter we wish to rename doesn't exist
        status, msg = model.rename_parameter("class1", "method1", "param_name7", "new_param_name")
        self.assertFalse(status)
        self.assertEqual(msg, " param_name7 does not exists in method1")

        # Ensure we get correct output when the parameter we wish to rename already exists
        status, msg = model.rename_parameter("class1", "method1", "param_name", "param_name")
        self.assertFalse(status)
        self.assertEqual(msg, " param_name already exists in method1")
        
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
        model.create_parameter("class1", "method1", "param_type", "parameter_name")
        testClass = model.classes["class1"]

        # Ensure we get correct output when class doesn't exist
        status, msg = model.delete_parameter("class9", "method1", "parameter_name")
        self.assertFalse(status)
        self.assertEqual(msg, "class9 does not exist")

        # Ensure we get correct output when method doesn't exist
        status, msg = model.delete_parameter("class1", "method6", "parameter_name")
        self.assertFalse(status)
        self.assertEqual(msg, "class1 does not have method, method6")
        
        # Ensure parameter is deleted
        status, msg = model.delete_parameter("class1", "method1", "parameter_name")
        self.assertFalse(testClass.methods[testClass.method_index("method1")].has_parameter("parameter_name"))

        # Ensure we get correct output after parameter is deleted
        self.assertTrue(status)
        self.assertEqual(msg, "parameter 'parameter_name' has been removed from 'method1'")

        # Ensure we get correct output if the parameter we wish to delete doesn't exist
        status, msg = model.delete_parameter("class1", "method1", "parameter_name")
        self.assertFalse(status)
        self.assertEqual(msg, " parameter_name does not exists in method1")

    ######################################################################

    # validates intended behavior of list_methods method
    def test_list_parameters(self):
        model = UMLModel()
        model.create_class("class1")
        
        # variables used for testing equality
        message = model.list_parameters("class2", "test")[1]
        # test output equality with using a non-existent class 
        self.assertEqual(message, "class2 does not exist")

        # variables used for testing equality
        message = model.list_parameters("class1", "test")[1]
        # test output equality without inserting methods 
        self.assertEqual(message, "class1 does not have method, test")

        # add some methods to class1
        model.create_method("class1", "public", "int", "getYear")
        # add some params to getYear
        model.create_parameter("class1", "getYear", "string", "calendarName")
        model.create_parameter("class1", "getYear", "int", "year")

        # variables used for testing equality
        message = model.list_parameters("class1", "getYear")[1]
        outString = "".join(("Parameters for getYear\n",
                            "(string):calendarName\n",  
                            "(int):year"))
        # test output equality            
        self.assertEqual(message,outString)
        
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

        status, msg = model.create_relationship("invalidRealType", "c5", "c2")
        self.assertFalse(status)
        self.assertEqual(msg, "'invalidRealType' is not a valid relationship type.")

        # Ensure we get correct output when class 1 doesn't exist
        status, msg = model.create_relationship("realization", "c5", "c2")
        self.assertFalse(status)
        self.assertEqual(msg, "'c5' does not exist")

        # Ensure we get correct output when class 2 doesn't exist
        status, msg = model.create_relationship("realization", "c1", "c5")
        self.assertFalse(status)
        self.assertEqual(msg, "'c5' does not exist")

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
        model.create_relationship("realization", "c1", "c2")

        # Ensure we get correct output when class 1 doesn't exist
        status, msg = model.delete_relationship("c7","c2")
        self.assertFalse(status)
        self.assertEqual(msg, "c7 does not exist")

        # Ensure we get correct output when class 2 doesn't exist
        status, msg = model.delete_relationship("c1","c5")
        self.assertFalse(status)
        self.assertEqual(msg, "c5 does not exist")

        # Ensure relationship is deleted
        status, msg = model.delete_relationship("c1","c2")
        self.assertEqual(len(model.classes["c1"].relationships), 0)
        self.assertEqual(len(model.classes["c2"].relationships), 0)
        
        # Ensure we get correct output after relationship has been deleted
        self.assertTrue(status)
        self.assertEqual(msg, "Relationship between c1 and c2 has been deleted")

        # Ensure we get correct output if we try to delete relationship that doesn't exist
        status, msg = model.delete_relationship("c1","c2")
        self.assertFalse(status)
        self.assertEqual(msg, "Relationship between c1 and c2 does not exist.")




    ######################################################################
    
    # validates intended behavior of move_up_relationship method
    def test_move_up_relationship(self):
        model = UMLModel()
        model.create_class("c1")
        model.create_class("c2")
        model.create_class("c3")
        model.create_class("c4")

        # Ensure relationship is created
        model.create_relationship("composition", "c1", "c2")
        self.assertTrue(model.classes["c1"].has_relationship("c2"))
        self.assertTrue(model.classes["c2"].has_relationship("c1"))

        # Ensure relationship is created
        model.create_relationship("aggregation", "c1", "c3")
        self.assertTrue(model.classes["c1"].has_relationship("c3"))
        self.assertTrue(model.classes["c3"].has_relationship("c1"))

        # Ensure relationship is created
        model.create_relationship("inheritance", "c1", "c4")
        self.assertTrue(model.classes["c1"].has_relationship("c4"))
        self.assertTrue(model.classes["c4"].has_relationship("c1"))

        # Ensure order of relationships for c1
        self.assertEqual(model.classes["c1"].relationship_index("c2"), 0)
        self.assertEqual(model.classes["c1"].relationship_index("c3"), 1)
        self.assertEqual(model.classes["c1"].relationship_index("c4"), 2)
        
        # Move c1's relationship with c4 up in c1
        model.move_up_relationship("c1", "c4")
        
        # Ensure the relationship was moved up 
        self.assertEqual(model.classes["c1"].relationship_index("c2"), 0)
        self.assertEqual(model.classes["c1"].relationship_index("c4"), 1)
        self.assertEqual(model.classes["c1"].relationship_index("c3"), 2)

        # Move c1's relationship with c4 up in c1
        model.move_up_relationship("c1", "c4")      

        # Ensure the relationship was moved up 
        self.assertEqual(model.classes["c1"].relationship_index("c4"), 0)  
        self.assertEqual(model.classes["c1"].relationship_index("c2"), 1)
        self.assertEqual(model.classes["c1"].relationship_index("c3"), 2)

        # Ensure correct response is outputted when we try to move a relationship
        # up when the relationship is at the top of the list
        status, msg = model.move_up_relationship("c1", "c4")
        self.assertFalse(status)
        self.assertEqual(msg, "The relationship with c4 can not move up any further in c1")

        # Ensure correct response is outputted when class 1 doesn't exist
        status, msg = model.move_up_relationship("c5", "c4")
        self.assertFalse(status)
        self.assertEqual(msg, "c5 does not exist")
        
        # Ensure correct response is outputted when class 2 doesn't exist
        status, msg = model.move_up_relationship("c1", "c7")
        self.assertFalse(status)
        self.assertEqual(msg, "c7 does not exist")

        # Ensure correct response is outputted when two classes don't have an
        # existing relationship
        status, msg = model.move_up_relationship("c2", "c3")
        self.assertFalse(status)
        self.assertEqual(msg, "Relationship between c2 and c3 does not exist.")
        
    ######################################################################

    # validate get_data
    def test_get_data(self):
        model = UMLModel()

        # Test 1: empty model
        data = model.get_data()
        self.assertEqual(data, {})

        # Test 2: model with data
        model.create_class('class1')
        model.create_class('class2')
        model.create_field('class1', 'private', 'string', 'name')
        expectedData = {
            "class1" : {
                "name" : "class1",
                "fields" : [{
                    "visibility" : 'private',
                    'type' : 'string',
                    'name' : 'name'
                }],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            },
            "class2" : {
                "name" : "class2",
                "fields" : [],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            }
        }
        data = model.get_data()
        self.assertEqual(data, expectedData)

    ######################################################################

    # validate set_data
    def test_set_data(self):
        model = UMLModel()
        
        # Test 1: set model data
        newData = {
            "class1" : {
                "name" : "class1",
                "fields" : [{
                    "visibility" : 'private',
                    'type' : 'string',
                    'name' : 'name'
                }],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            },
            "class2" : {
                "name" : "class2",
                "fields" : [],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            }
        }
        status, msg = model.set_data(newData)
        self.assertTrue(status)
        # ensure each piece was copied in correctly
        # ensure classes were created
        self.assertTrue("class1" in model.classes)
        self.assertTrue("class2" in model.classes)
        status, msg = model.list_fields("class1")
        self.assertEqual(msg, "Fields of class1\nPRIVATE string name")

        # Test 2: invalid data 
        badData = {
            "class1" : "somethings not right here..."
        }
        status, msg = model.set_data(badData)
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "Data cannot be parsed")
        # ensure previous model is still there
        self.assertTrue("class1" in model.classes)
        self.assertTrue("class2" in model.classes)
        status, msg = model.list_fields("class1")
        self.assertEqual(msg, "Fields of class1\nPRIVATE string name")

        # Test 3: invalid data - type error
        badData = {
            "class1" : {
                "name" : "class1",
                "fields": [7]
            }
        }
        status, msg = model.set_data(badData)
        print(model.list_class("class1"))
        # ensure it failed
        self.assertFalse(status)
        self.assertEqual(msg, "Data cannot be parsed")
        # ensure previous model is still there
        self.assertTrue("class1" in model.classes)
        self.assertTrue("class2" in model.classes)
        status, msg = model.list_fields("class1")
        self.assertEqual(msg, "Fields of class1\nPRIVATE string name")
        
    ######################################################################

    # validate save_model
    def test_save_model(self):
        model = UMLModel()
        model.create_class('class1')
        model.create_class('class2')
        model.create_class('class3')
        model.create_field('class1', "protected", "int", "number")
        model.create_method('class2', "public", "string", "getMsg")
        model.create_parameter('class2', 'getMsg', 'string', 'msg')

        # Test 1: Normal save
        model.save_model("test-save.json")
        # ensure data is in the json file
        data = None
        with open("code/server-data/test-save.json", 'r') as file:
            data = json.loads(file.read())
        expectedData = {
            "class1" : {
                "name" : "class1",
                "fields" : [{
                    "visibility" : "protected",
                    "type" : "int",
                    "name" : "number"
                }],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            },
            "class2" : {
                "name" : "class2",
                "fields" : [],
                "methods" : [{
                    "visibility" : "public",
                    "type" : "string",
                    "name" : "getMsg",
                    "parameters" : [{
                        'type' : 'string',
                        'name' : 'msg'
                    }]
                }],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            },
            "class3" : {
                "name" : "class3",
                "fields" : [],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            }
        }
        self.assertEqual(data, expectedData)

        # Test 2: save to different directory
        directory = os.getcwd() + '/'
        model.save_model("test-save2.json", directory=directory)
        data = None
        passes = True
        try:
            with open("test-save2.json", 'r') as file:
                data = json.loads(file.read())
        except FileNotFoundError:
            passes = False
        self.assertTrue(passes)
        self.assertEqual(data, expectedData)

    ######################################################################

    # validate load_model
    def test_load_model(self):
        
        expectedData = {
            "class1" : {
                "name" : "class1",
                "fields" : [{
                    "visibility" : "protected",
                    "type" : "int",
                    "name" : "number"
                }],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            },
            "class2" : {
                "name" : "class2",
                "fields" : [],
                "methods" : [{
                    "visibility" : "public",
                    "type" : "string",
                    "name" : "getMsg",
                    "parameters" : [{
                        'type' : 'string',
                        'name' : 'msg'
                    }]
                }],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            },
            "class3" : {
                "name" : "class3",
                "fields" : [],
                "methods" : [],
                "relationships" : [],
                "x" : 200,
                "y" : 0,
                "zindex" : 0
            }
        }
        json_data = json.dumps(expectedData, indent=4)
        with open("code/server-data/test-load.json", "w") as file:
            file.write(json_data)

        # Test 1: load empty model
        model = UMLModel()
        model.load_model("test-load.json")
        # ensure data was loaded properly
        self.assertEqual(expectedData, model.get_data())

        # Test 2: load invalid data
        json_data = json.dumps({"class1": "toast"}, indent=4)
        with open("code/server-data/test-load.json", "w") as file:
            file.write(json_data)

        model = UMLModel()
        status, msg = model.load_model("test-load.json")
        # ensure data wasn't loaded
        self.assertEqual({}, model.get_data())
        self.assertFalse(status)

        # Test 3: load non-json-parsable file
        non_json_data = "not json data"
        with open("code/server-data/test-load.json", "w") as file:
            file.write(non_json_data)

        model = UMLModel()
        status, msg = model.load_model("test-load.json")
        # ensure data wasn't loaded
        self.assertEqual({}, model.get_data())
        self.assertFalse(status)

        # Test 4: load file that doesn't exist
        model = UMLModel()
        status, msg = model.load_model("iDontExist.json")
        # ensure data wasn't loaded
        self.assertEqual({}, model.get_data())
        self.assertFalse(status)

    # validates intended behavior of move_down_relationship method
    def test_move_down_relationship(self):
        model = UMLModel()
        model.create_class("c1")
        model.create_class("c2")
        model.create_class("c3")
        model.create_class("c4")

        # Ensure relationship is created
        model.create_relationship("composition", "c1", "c2")
        self.assertTrue(model.classes["c1"].has_relationship("c2"))
        self.assertTrue(model.classes["c2"].has_relationship("c1"))

        # Ensure relationship is created
        model.create_relationship("aggregation", "c1", "c3")
        self.assertTrue(model.classes["c1"].has_relationship("c3"))
        self.assertTrue(model.classes["c3"].has_relationship("c1"))

        # Ensure relationship is created
        model.create_relationship("inheritance", "c1", "c4")
        self.assertTrue(model.classes["c1"].has_relationship("c4"))
        self.assertTrue(model.classes["c4"].has_relationship("c1"))

        # Ensure order of relationships for c1
        self.assertEqual(model.classes["c1"].relationship_index("c2"), 0)
        self.assertEqual(model.classes["c1"].relationship_index("c3"), 1)
        self.assertEqual(model.classes["c1"].relationship_index("c4"), 2)
        
        # Move c1's relationship with c2 down in c1
        model.move_down_relationship("c1", "c2")
        
        # Ensure the relationship was moved down 
        self.assertEqual(model.classes["c1"].relationship_index("c3"), 0)
        self.assertEqual(model.classes["c1"].relationship_index("c2"), 1)
        self.assertEqual(model.classes["c1"].relationship_index("c4"), 2)

        # Move c1's relationship with c2 down in c1
        model.move_down_relationship("c1", "c2")      

        # Ensure the relationship was moved down 
        self.assertEqual(model.classes["c1"].relationship_index("c3"), 0)
        self.assertEqual(model.classes["c1"].relationship_index("c4"), 1)
        self.assertEqual(model.classes["c1"].relationship_index("c2"), 2)

        # Ensure correct response is outputted when we try to move a relationship
        # down when the relationship is at the bottom of the list
        status, msg = model.move_down_relationship("c1", "c2") 
        self.assertFalse(status)
        self.assertEqual(msg, "The relationship with c2 can not move down any further in c1")

        # Ensure correct response is outputted when class 1 doesn't exist
        status, msg = model.move_down_relationship("c5", "c2")
        self.assertFalse(status)
        self.assertEqual(msg, "c5 does not exist")
        
        # Ensure correct response is outputted when class 2 doesn't exist
        status, msg = model.move_down_relationship("c1", "c7")
        self.assertFalse(status)
        self.assertEqual(msg, "c7 does not exist")

        # Ensure correct response is outputted when two classes don't have an
        # existing relationship
        status, msg = model.move_down_relationship("c2", "c3")
        self.assertFalse(status)
        self.assertEqual(msg, "Relationship between c2 and c3 does not exist.")

    ######################################################################

    # validates intended behavior of list_relationships method
    def test_list_relationships(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_class("class2")

        # variables used for testing equality
        message = model.list_relationships("class5")[1]
        # test output equality with using a non-existent class name
        self.assertEqual(message, "class5 does not exist")
        
        # test with a parameter
        # variables used for testing equality
        message = model.list_relationships('class1')[1]
        # test output equality without creating a relationship
        self.assertEqual(message, "Class 'class1' has no relationships")

        # test without a parameter
        # variables used for testing equality
        message = model.list_relationships()[1]
        # test output equality without creating a relationship
        self.assertEqual(message, "No relationships exist for the current model")

        # create a relationship between the classes
        model.create_relationship("inheritance", "class1", "class2")

        # test with a parameter
        message = model.list_relationships("class1")[1]
        # test output equality
        outString = "".join(("Relationships for class1\n",
                             "class1 ---------> class2"))
        self.assertEqual(message, outString)

        # test without a parameter
        # variables used for testing equality
        message = model.list_relationships()[1]
        outString = "".join(("Listing all relationships\n",
                             "class1 ---------> class2\n",
                             "class2 <--------- class1"))
        # test output equality            
        self.assertEqual(message,outString)

    ######################################################################
# runs all of our tests
# allows us to run this file using the typical 'python3 test_UMLModel.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLModel.py' command
if __name__ == '__main__':
    unittest.main()
