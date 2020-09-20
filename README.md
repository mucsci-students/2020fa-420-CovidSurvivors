UMLEditor
=========

UMLEditor is a simple Command-Line editor for working in a Unified Modeling Language (`UML`_). 

Currently, the program allows for creating and deleting classes, attributes, and relationships. The program also allows for saving and loading models. 

Installing
----------

Download the repository from our GitHub Page:
https://github.com/mucsci-students/2020fa-420-CovidSurvivors

Running The Program
-------------------

You must have python3 installed to run the program. You can install it using:
.. code-block:: text
    $ sudo apt-get install python3

In a terminal, navigate to the UMLEditor code folder. Type the below command to start up the Command-Line based version of the UMLEditor.

.. code-block:: text
    python3 UMLEditor.py

From there you should have entered the UMLEditor and you should see a prompt like below:
.. code-block:: text
    UMLEditor> 

A Simple Example
----------------

You can type 'help' to see a list of commands. 

.. code-block:: text
    UMLEditor> create_class myclass1
    UMLEditor> create_class myclass2
    UMLEditor> create_attribute myclass1 myattrib1
    UMLEditor> create_attribute myclass1 myattrib2
    UMLEditor> create_attribute myclass2 myattrib3

.. code-block:: text
    UMLEditor> list_classes
    myclass1
    myclass2
    UMLEditor> list_attributes myclass1
    myattrib1
    myattrib2
    UMLEditor> list_attributes myclass2
    myattrib3

Saving and Loading Models
-------------------------

In the UMLEditor, a model can be saved to a specified JSON file 
.. code-block:: text
    UMLEditor> save_model MyModel.json

This will save all the data for the model to the specified JSON file and store it in the models directory. 

A model can later be loaded back into the program and edited. 
.. code-block:: text
    UMLEditor> load_model MyModel.json


Links
-----

* Code: https://github.com/mucsci-students/2020fa-420-CovidSurvivors

.. _UML: https://en.wikipedia.org/wiki/Unified_Modeling_Language