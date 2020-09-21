UMLEditor
=========

UMLEditor is a simple Command-Line editor for working in a [Unified Modeling Language](https://en.wikipedia.org/wiki/Unified_Modeling_Language). 

Currently, the program allows for creating and deleting classes, attributes, and relationships. The program also allows for saving and loading models. 

Installing
----------

Download the repository from our GitHub Page:
https://github.com/mucsci-students/2020fa-420-CovidSurvivors

Running The Program
-------------------

You must have python3 installed to run the program. You can install it using:
```
$ sudo apt-get install python3
```

In a terminal, navigate to the UMLEditor code folder. Type the below command to start up the Command-Line based version of the UMLEditor.

```
$ python3 UMLEditor.py
```

From there you should have entered the UMLEditor and you should see a prompt like below:
```
UMLEditor> 
```

A Simple Example
----------------

You can type 'help' to see a list of commands. 
Here is a simple example:

```
UMLEditor> create_class myClass1
UMLEditor> create_class myClass2
UMLEditor> create_attribute myClass1 myAttrib1
UMLEditor> create_attribute myClass1 myAttrib2
UMLEditor> create_attribute myClass2 myAttrib3
```
```
UMLEditor> list_classes
myClass1
myClass2
UMLEditor> list_attributes myClass1
myAttrib1
myAttrib2
UMLEditor> list_attributes myClass2
myAttrib3
```

Saving and Loading Models
-------------------------

In the UMLEditor, a model can be saved to a specified JSON file 
```
UMLEditor> save_model MyModel.json
```

This will save all the data for the model to the specified JSON file and store it in the models directory. 

A model can later be loaded back into the program and edited. But you must remember to save it to apply the changes. 

```
UMLEditor> load_model MyModel.json
```

Links
-----

* Code: https://github.com/mucsci-students/2020fa-420-CovidSurvivors
