# Unit test for the UMLModel class
# Description:     
#   This file validates that each function belonging to the UMLModel class behaves as intended
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 20, 2020

##########################################################################
# Imports

import unittest
import sys
sys.path.append('../')
from UMLModel import UMLModel
import io 

##########################################################################

# Unit test for the UMLModel

class UMLModelTest(unittest.TestCase):

    def test_create_class(self):

        model = UMLModel()

        # Ensure class is created
        model.create_class("class1")
        self.assertEqual(model.classes["class1"].name, "class1")

        # Ensure duplicate class is not created 
        # use io capture to grab output of create_class
        captured = io.StringIO()
        sys.stdout = captured
        model.create_class("class1")
        self.assertEqual(captured.getvalue(), "class1 already exists.\n")

    ######################################################################

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
        captured = io.StringIO()
        sys.stdout = captured
        model.rename_class("class1", "classB")
        self.assertEqual(captured.getvalue(), "class1 does not exist.\n")

        # Ensure duplicate newname is rejected
        model.create_class("class1")
        captured = io.StringIO()
        sys.stdout = captured
        model.rename_class("classA", "class1")
        self.assertEqual(captured.getvalue(), "class1 already exists.\n")

    ######################################################################

    def test_delete_class(self):

        model = UMLModel()
        model.create_class("class1")

        # Ensure deleted 
        model.delete_class("class1")
        # assert dictionary key was removed
        self.assertTrue("class1" not in model.classes)

        # Ensure no errors when class DNE
        captured = io.StringIO()
        sys.stdout = captured
        model.delete_class("class1")
        self.assertEqual(captured.getvalue(), "class1 does not exist.\n")

    ######################################################################
    
    def test_create_attribute(self):
        model = UMLModel()
        model.create_class("class1")

        # Ensure attrib is created
        model.create_attribute("class1", "a1")
        self.assertTrue("a1" in model.classes["class1"].attributes)

        # Ensure duplicate attrib is not created 
        # use io capture to grab output of create_class
        captured = io.StringIO()
        sys.stdout = captured
        model.create_attribute("class1", "a1")
        self.assertEqual(captured.getvalue(), "a1 already exists in class1\n")

    ######################################################################

    def test_rename_attribute(self):
        model = UMLModel()
        model.create_class("class1")
        model.create_attribute("class1", "a1")

        # Ensure attrib is renamed
        model.rename_attribute("class1", "a1", "a2")
        self.assertTrue("a1" not in model.classes["class1"].attributes)
        self.assertTrue("a2" in model.classes["class1"].attributes)

    ######################################################################

    def test_delete_attribute(self):
        model = UMLModel()
        model.create_class("class1")

        # Ensure attrib is deleted
        model.delete_attribute("class1", "a1")
        self.assertTrue("a1" not in model.classes["class1"].attributes)

    ######################################################################

    def test_create_relationship(self):
        model = UMLModel()
        model.create_class("c1")
        model.create_class("c2")

        # Ensure relationship is created
        model.create_relationship("r1", "c1", "c2")
        self.assertEqual(model.classes["c1"].relationships[0].class1.name, "c1")
        self.assertEqual(model.classes["c1"].relationships[0].class2.name, "c2")
        self.assertEqual(model.classes["c2"].relationships[0].class1.name, "c1")
        self.assertEqual(model.classes["c2"].relationships[0].class2.name, "c2")

        # Ensure already existing rel 
        captured = io.StringIO()
        sys.stdout = captured
        model.create_relationship("r1","c2","c1")
        self.assertEqual(captured.getvalue(), "Relationship between c2 and c1 already exists.\n")

    ######################################################################

    def test_delete_relationship(self):
        model = UMLModel()
        model.create_class("c1")
        model.create_class("c2")
        model.create_relationship("r1", "c1", "c2")

        # Ensure relationship is created
        model.delete_relationship("c1","c2")
        self.assertEqual(len(model.classes["c1"].relationships), 0)
        self.assertEqual(len(model.classes["c2"].relationships), 0)
        
##########################################################################

# runs all of our tests 
# allows us to run this file using the typical 'python3 test_UMLModel.py' command
# without it, we would have to use the 'python3 -m unittest test_UMLModel.py' command
if __name__ == '__main__':
    unittest.main()