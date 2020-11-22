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
        with open("code/data/test-save.json", 'r') as file:
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
        with open("code/data/test-load.json", "w") as file:
            file.write(json_data)

        # Test 1: load empty model
        model = UMLModel()
        model.load_model("test-load.json")
        # ensure data was loaded properly
        self.assertEqual(expectedData, model.get_data())

        # Test 2: load invalid data
        json_data = json.dumps({"class1": "toast"}, indent=4)
        with open("code/data/test-load.json", "w") as file:
            file.write(json_data)

        model = UMLModel()
        status, msg = model.load_model("test-load.json")
        # ensure data wasn't loaded
        self.assertEqual({}, model.get_data())
        self.assertFalse(status)

        # Test 3: load non-json-parsable file
        non_json_data = "not json data"
        with open("code/data/test-load.json", "w") as file:
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

    ######################################################################
   
# runs all of our tests
# allows us to run this file using the typical 'python3 test_UMLModel.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLModel.py' command
if __name__ == '__main__':
    unittest.main()
