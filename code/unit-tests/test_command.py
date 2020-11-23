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
        "parameter_names" : [],
        "relationship_types" : [],
        "relationship_others" : []
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
        "parameter_names" : [],
        "relationship_types" : [],
        "relationship_others" : []
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
