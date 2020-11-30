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
from models.RelationshipType import RelationshipType
import io
from command.command import *

##########################################################################

class CreateClassGUICommandTest(unittest.TestCase):

    def test_execute(self):

        # create model 
        model_name = "myModel"
        model = UMLModel()
        model.save_model(model_name + ".json", directory=os.getcwd() + "/")

        class_data = {
        "filename" : model_name + ".json",
        "directory" : os.getcwd() + "/",
        "class_name" : "class1",
        "field_visibilities" : ["private", "private"],
        "field_types" : ["string", "int"],
        "field_names" : ["name", "age"],
        "method_visibilities" : ["public"],
        "method_types" : ["string"],
        "method_names" : ["getName"],
        "parameter_method_index" : [],
        "parameter_types" : [],
        "parameter_names" : []
        }

        cmd = CreateClassGUICommand(model, class_data)

        cmd.saveBackup()

        status, msg = cmd.execute()

        # ensure it passed
        self.assertTrue(status)

        # ensure components are in model
        self.assertTrue("class1" in model.classes)
        self.assertTrue(len(model.classes["class1"].fields) == 2)

##########################################################################

class EditClassGUICommandTest(unittest.TestCase):

    def test_execute(self):

        # create model 
        model_name = "myModel"
        model = UMLModel()
        model.create_class("class1")
        model.save_model(model_name + ".json", directory=os.getcwd() + "/")

        class_data = {
        "filename" : model_name + ".json",
        "directory" : os.getcwd() + "/",
        "original_name" : "class1",
        "class_name" : "class2",
        "field_visibilities" : ["private", "private"],
        "field_types" : ["string", "int"],
        "field_names" : ["name", "age"],
        "method_visibilities" : ["public"],
        "method_types" : ["string"],
        "method_names" : ["getName"],
        "parameter_method_index" : [],
        "parameter_types" : [],
        "parameter_names" : []
        }

        cmd = EditClassGUICommand(model, class_data)

        cmd.saveBackup()

        status, msg = cmd.execute()

        # ensure it passed
        self.assertTrue(status)

        # ensure components are in model
        self.assertTrue("class2" in model.classes)
        self.assertTrue(len(model.classes["class2"].fields) == 2)

##########################################################################

class CreateRelationshipGUICommandTest(unittest.TestCase):

    def test_execute(self):

        # create model 
        model_name = "myModel"
        model = UMLModel()
        model.create_class("class1")
        model.create_class("class2")
        model.save_model(model_name + ".json", directory=os.getcwd() + "/")

        class_data = {
        "filename" : model_name + ".json",
        "directory" : os.getcwd() + "/",
        "relationship_type" : "inheritance",
        "class_name1" : "class1",
        "class_name2" : "class2"
        }

        cmd = CreateRelationshipGUICommand(model, class_data)
        cmd.saveBackup()
        status, msg = cmd.execute()
        # ensure it passed
        self.assertTrue(status)
        # relationship exists
        self.assertTrue(len(model.classes["class1"].relationships) == 1)
        self.assertTrue(len(model.classes["class2"].relationships) == 1)
        self.assertEqual(model.classes["class1"].relationships[0].type, RelationshipType.INHERITANCE)
        self.assertEqual(model.classes["class1"].relationships[0].other, "class2")
        self.assertEqual(model.classes["class2"].relationships[0].other, "class1")

        # ensure it fails when invalid
        cmd = CreateRelationshipGUICommand(model, class_data)
        cmd.saveBackup()
        status, msg = cmd.execute()

        self.assertFalse(status)

##########################################################################

class EditRelationshipGUICommandTest(unittest.TestCase):

    def test_execute(self):

        # create model 
        model_name = "myModel"
        model = UMLModel()
        model.create_class("class1")
        model.create_class("class2")
        model.create_relationship("composition", "class1", "class2")
        model.save_model(model_name + ".json", directory=os.getcwd() + "/")

        class_data = {
        "filename" : model_name + ".json",
        "directory" : os.getcwd() + "/",
        "old_relationship_type" : "composition",
        "old_class_name1" : "class1",
        "old_class_name2" : "class2",
        "relationship_type" : "inheritance",
        "class_name1" : "class1",
        "class_name2" : "class2"
        }

        cmd = EditRelationshipGUICommand(model, class_data)
        cmd.saveBackup()
        status, msg = cmd.execute()
        # ensure it passed
        self.assertTrue(status)
        # relationship exists
        self.assertTrue(len(model.classes["class1"].relationships) == 1)
        self.assertTrue(len(model.classes["class2"].relationships) == 1)
        self.assertEqual(model.classes["class1"].relationships[0].type, RelationshipType.INHERITANCE)
        self.assertEqual(model.classes["class1"].relationships[0].other, "class2")
        self.assertEqual(model.classes["class2"].relationships[0].other, "class1")

        # ensure it fails when invalid
        class_data["class_name2"] = "invalid_class"
        cmd = EditRelationshipGUICommand(model, class_data)
        cmd.saveBackup()
        status, msg = cmd.execute()

        self.assertFalse(status)

##########################################################################

class DeleteRelationshipGUICommandTest(unittest.TestCase):

    def test_execute(self):

        # create model 
        model_name = "myModel"
        model = UMLModel()
        model.create_class("class1")
        model.create_class("class2")
        model.create_relationship("composition", "class1", "class2")
        model.save_model(model_name + ".json", directory=os.getcwd() + "/")

        class_data = {
        "filename" : model_name + ".json",
        "directory" : os.getcwd() + "/",
        "class_name1" : "class1",
        "class_name2" : "class2"
        }

        cmd = DeleteRelationshipGUICommand(model, class_data)
        cmd.saveBackup()
        status, msg = cmd.execute()
        # ensure it passed
        self.assertTrue(status)
        # ensure relationship was deleted
        self.assertTrue(len(model.classes["class1"].relationships) == 0)
        self.assertTrue(len(model.classes["class2"].relationships) == 0)

        # ensure it fails when invalid
        cmd = DeleteRelationshipGUICommand(model, class_data)
        cmd.saveBackup()
        status, msg = cmd.execute()

        self.assertFalse(status)

##########################################################################
