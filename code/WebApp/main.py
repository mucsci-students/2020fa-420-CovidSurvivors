# Flask Server for UMLEditor GUI
# Description:     
#   This file uses Flask to serve up files for out GUI 
#   This acts as our main Controller of the GUI
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     November 17 2020
##########################################################################
# Imports

import os
import sys
import json
from flask import Flask, render_template, send_file, request
from flask import url_for, redirect, flash
from werkzeug.utils import secure_filename

# Include parent directory
sys.path.append(os.getcwd())
from command.command import *
from models.UMLModel import UMLModel

##########################################################################
# Globals 

app = Flask(__name__)

app.config['SECRET_KEY'] = '2ca8690a209df45699ccf028b6a47015'

# Where the data model is saved
DATA_FOLDER = os.path.join(os.getcwd(), 'server-data/')
# The name of the server's current working model file
WORKING_FILENAME = '__WorkingModel__.json'
TEMP_FILENAME = '__temp__.json'
HISTORY_LIMIT = 20

# keeps track of prior commands 
command_history = CommandHistory(HISTORY_LIMIT)

##########################################################################

def getModelNames():
    """Returns a list of the model names 
    """
    # Grab model info
    models = list(os.listdir(DATA_FOLDER))

    # remove server files
    models = [filename for filename in models if filename != "__WorkingModel__.json" and filename != "__temp__.json"]

    # remove json extension
    models = [filename[:-5] for filename in models]

    return models

##########################################################################

# The main page 
# where you select which model you want to edit 
@app.route("/")
@app.route("/models")
def models():
    # sort for clean order
    # OS files for some reason are in an unknown order
    models = sorted(getModelNames())
    return render_template("models.html", models=models)

##########################################################################

@app.route("/createModel", methods=["GET", "POST"])
def createModel():
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('models'))

    model_name:str = request.form.get("model_name")

    # Ensure new model name does not already exist
    if model_name in getModelNames():
        flash(f"Model '{request.form.get('model_name')}' already exists", "error")
        return redirect(url_for('models'))

    # reject empty model names
    if model_name.strip() == "":
        flash(f"Model name cannot be empty", "error")
        return redirect(url_for('models'))

    # create new empty model file
    model = UMLModel()
    model.save_model(model_name + ".json", directory=DATA_FOLDER)
    
    flash(f"Model '{model_name}' created successfully", "success")
    return redirect(url_for("models"))

##########################################################################

@app.route("/renameModel", methods=["GET", "POST"])
def renameModel():
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('models'))

    old_model_name:str = request.form.get("old_model_name")
    new_model_name:str = request.form.get("new_model_name")

    # ensure model name exists
    if old_model_name not in getModelNames():
        flash(f"Model '{old_model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # ensure new model name does not exist 
    if new_model_name in getModelNames():
        flash(f"Model '{new_model_name}' already exists", "error")
        return redirect(url_for('models'))
    
    # reject empty model names
    if new_model_name.strip() == "":
        flash(f"Model name cannot be empty", "error")
        return redirect(url_for('models'))


    old_model_file_name = "".join([DATA_FOLDER, old_model_name, ".json"])
    new_model_file_name = "".join([DATA_FOLDER, new_model_name, ".json"])

    os.rename(old_model_file_name, new_model_file_name)

    flash(f"Model '{old_model_name}' successfully renamed to '{new_model_name}'", "success")
    return redirect(url_for("models"))

##########################################################################

@app.route("/deleteModel", methods=["GET", "POST"])
def deleteModel():
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('models'))

    model_name = request.form.get("model_name")

    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    model_filename = "".join([DATA_FOLDER, model_name, ".json"])

    # remove the model
    os.remove(model_filename)

    flash(f"Model '{model_name}' successfully deleted", "success")
    return redirect(url_for("models"))

##########################################################################

# The model editing page
@app.route("/model/<model_name>")
def dashboard(model_name):

    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # Get current model
    model = UMLModel()
    status, msg = model.load_model(model_name + ".json", directory=DATA_FOLDER)

    if not status:
        flash(msg, "error")
        return render_template("dashboard.html", data={})

    # Setup template data
    data = {
        "model_name" : model_name,
        "classes" : []
    }

    # add each class
    i = 0 
    for class_name in model.classes:
        data["classes"] += [model.classes[class_name].get_raw_data()]
        # Give class its index 
        data["classes"][i]["index"] = i+1
        data["classes"][i]["json"] = json.dumps(model.classes[class_name].get_raw_data())
        i += 1

    return render_template("dashboard.html", data=data)

##########################################################################

# Creates a class from the given class data in POST request
@app.route("/model/<model_name>/createClass", methods=["GET", "POST"])
def createClass(model_name):

    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard'))

    # Grab the data from the POST request 
    # and structure it for the command
    class_data = {
        "filename" : model_name + ".json",
        "directory" : DATA_FOLDER,
        "class_name" : request.form.get('class_name'),
        "field_visibilities" : list(request.form.getlist('field_visibility')),
        "field_types" : list(request.form.getlist('field_type')),
        "field_names" : list(request.form.getlist('field_name')),
        "method_visibilities" : list(request.form.getlist('method_visibility')),
        "method_types" : list(request.form.getlist('method_type')),
        "method_names" : list(request.form.getlist('method_name')),
        "parameter_method_index" : list(request.form.getlist('parameter_method')),
        "parameter_types" : list(request.form.getlist('parameter_type')),
        "parameter_names" : list(request.form.getlist('parameter_name'))
    }

    # create command 
    command = CreateClassGUICommand(UMLModel(), class_data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard', model_name=model_name))

##########################################################################

# Edits an existing class
@app.route("/model/<model_name>/editClass", methods=["GET", "POST"])
def editClass(model_name):

    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # Create new class with new data
    # Grab the data from the POST request 
    class_data = {
        "filename" : model_name + ".json",
        "directory" : DATA_FOLDER,
        "original_name" : request.form.get('original_name'),
        "class_name" : request.form.get('class_name'),
        "field_visibilities" : list(request.form.getlist('field_visibility')),
        "field_types" : list(request.form.getlist('field_type')),
        "field_names" : list(request.form.getlist('field_name')),
        "method_visibilities" : list(request.form.getlist('method_visibility')),
        "method_types" : list(request.form.getlist('method_type')),
        "method_names" : list(request.form.getlist('method_name')),
        "parameter_method_index" : list(request.form.getlist('parameter_method')),
        "parameter_types" : list(request.form.getlist('parameter_type')),
        "parameter_names" : list(request.form.getlist('parameter_name'))
    }

    # create command 
    command = EditClassGUICommand(UMLModel(), class_data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response - this occurs if someone forgot to return a status from a command
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard', model_name=model_name))

##########################################################################

# Serves the contents of the modal with a given class_name
# This is for the edit modal
@app.route("/model/<model_name>/editForm", methods=['GET', 'POST'])
def editForm(model_name):
    
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))
    
    # load model
    model = UMLModel()
    model.load_model(model_name + ".json", directory=DATA_FOLDER)

    # ensure class exists
    if request.form.get('class_name') not in model.classes:
        return f"Class '{request.form.get('class_name')}' does not exist"

    # grab class data
    data = model.classes[request.form.get('class_name')].get_raw_data()

    # index methods for parameter matching
    for class_name in data:
        i = 0
        for methodi in range(len(data["methods"])):
            data["methods"][methodi]["index"] = i
            i+=1

    # Build modal form inputs
    return render_template("modalForm.html", data=data)

##########################################################################

# creates a relationship with a given relationship type, and two class names
@app.route("/model/<model_name>/createRelationship", methods=['POST'])
def createRelationship(model_name):
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))
        
    
    # build data for command
    data = {
        "filename" : model_name + ".json",
        "directory" : DATA_FOLDER,
        "relationship_type" : request.form.get('relationship_type'),
        "class_name1" : request.form.get('class_name1'),
        "class_name2" : request.form.get('class_name2')
    }

    # create command 
    command = CreateRelationshipGUICommand(UMLModel(), data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response - this occurs if someone forgot to return a status from a command
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard', model_name=model_name))

##########################################################################

# creates a relationship with a given relationship type, and two class names
@app.route("/model/<model_name>/editRelationship", methods=['POST'])
def editRelationship(model_name):
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))
        
    # build data for command
    data = {
        "filename" : model_name + ".json",
        "directory" : DATA_FOLDER,
        "old_relationship_type" : request.form.get('old_relationship_type'),
        "old_class_name1" : request.form.get('old_class_name1'),
        "old_class_name2" : request.form.get('old_class_name2'),
        "relationship_type" : request.form.get('relationship_type'),
        "class_name1" : request.form.get('class_name1'),
        "class_name2" : request.form.get('class_name2')
    }

    # create command 
    command = EditRelationshipGUICommand(UMLModel(), data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response - this occurs if someone forgot to return a status from a command
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard', model_name=model_name))

##########################################################################

# creates a relationship with a given relationship type, and two class names
@app.route("/model/<model_name>/deleteRelationship", methods=['POST'])
def deleteRelationship(model_name):
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))
        
    # build data for command
    data = {
        "filename" : model_name + ".json",
        "directory" : DATA_FOLDER,
        "class_name1" : request.form.get('class_name1'),
        "class_name2" : request.form.get('class_name2')
    }

    # create command 
    command = DeleteRelationshipGUICommand(UMLModel(), data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response - this occurs if someone forgot to return a status from a command
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard', model_name=model_name))

##########################################################################

# Serves the contents of the modal 
@app.route("/model/<model_name>/editRelationshipForm", methods=['GET', 'POST'])
def editRelationshipForm(model_name):
    
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))
    
    # load model
    model = UMLModel()
    model.load_model(model_name + ".json", directory=DATA_FOLDER)

    # ensure class1 exists
    if request.form.get('class_name1') not in model.classes:
        return f"Class '{request.form.get('class_name1')}' does not exist"
    # ensure class2 exists
    if request.form.get('class_name2') not in model.classes:
        return f"Class '{request.form.get('class_name2')}' does not exist"

    # grab class data
    data = {}
    data["classes"] = model.get_data()

    # add current relationships data
    data["relationship_type"] = request.form.get('relationship_type')
    data["class_name1"] = request.form.get('class_name1')
    data["class_name2"] = request.form.get('class_name2')

    # Build modal form inputs
    return render_template("editRelationshipForm.html", data=data)

##########################################################################

# Saves the position of a class card based on its location on the dashboard
@app.route("/model/<model_name>/saveCardPosition", methods=['POST'])
def saveCardPosition(model_name):
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # load model
    model = UMLModel()
    model.load_model(model_name + ".json", directory=DATA_FOLDER)

    # Grab the position data from the POST request 
    class_data = {
        "filename" : model_name + ".json",
        "directory" : DATA_FOLDER,
        "class_name" : request.form['class_name'],
        "x" : request.form['x'],
        "y": request.form['y'],
        "zindex": request.form['zindex']
    }

    # create command 
    command = SetClassPositonGUICommand(UMLModel(), class_data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response - this occurs if someone forgot to return a status from a command
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard', model_name=model_name))


##########################################################################

# Server for deleting a class
@app.route("/model/<model_name>/deleteClass", methods=["GET", "POST"])
def deleteClass(model_name):

    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # Ensure method was post
    if request.method != 'POST':
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # Print out what is being deleted
    print (f"Deleting class '{request.form.get('class_name')}' from the model")
    
    # Grab the data from the POST request 
    class_data = {
        "filename" : model_name + ".json",
        "directory" : DATA_FOLDER,
        "class_name" : request.form.get('class_name')
    }
    
    # create command 
    command = DeleteClassGUICommand(UMLModel(), class_data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard', model_name=model_name))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard', model_name=model_name))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard', model_name=model_name))


##########################################################################

# Undoes a previously executed command
@app.route("/model/<model_name>/undo")
def undo(model_name):

    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # get undoable command
    command = command_history.pop_undo()

    # ensure there was a command
    if command == None:
        # send error message as a flash message
        flash("Nothing to undo", "error")
        return redirect(url_for('dashboard', model_name=model_name))
    
    # undo the command
    command.undo()

    # send success message as a flash message
    print(f"SUCCESS: Successfully undid last command")
    flash("Undo successful", "success")
    return redirect(url_for('dashboard', model_name=model_name))

##########################################################################

# redo a previously undone command
@app.route("/model/<model_name>/redo")
def redo(model_name):
    
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    # get undone command
    command = command_history.pop_redo()

    # ensure there was a command
    if command == None:
        # send error message as a flash message
        flash("Nothing to redo", "error")
        return redirect(url_for('dashboard', model_name=model_name))
    
    # redo the command
    command.execute()

    # send success message as a flash message
    print(f"SUCCESS: Redo successful")
    flash("Redo successful", "success")
    return redirect(url_for('dashboard', model_name=model_name))

##########################################################################

# Server for Downloading models 
@app.route("/model/<model_name>/download")
def download(model_name):
    
    # ensure model name exists
    if model_name not in getModelNames():
        flash(f"Model '{model_name}' does not exist", "error")
        return redirect(url_for('models'))

    return send_file(DATA_FOLDER + model_name + ".json")

##########################################################################

# Returns whether or not the filename has the json extension
def is_json(filename):
    # Ensure file has an extension
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension == 'json'

# Server for uploading a model 
# The current working model is replaced with the 
# data of the inputted model 
@app.route("/upload", methods=["GET", "POST"])
def upload():
    # Ensure there was a POST request
    if request.method != 'POST':
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('models'))

    # Ensure POST has a 'file' 
    if 'file' not in request.files:
        # send error message as a flash message
        flash("No file provided", "error")
        return redirect(url_for('models'))
    
    # Ensure filename does not already exist
    if request.form.get("model_name") in getModelNames():
        flash(f"Model '{request.form.get('model_name')}' already exists", "error")
        return redirect(url_for('models'))

    # Grab file
    file = request.files['file']

    # Ensure there was a file submitted
    if file.filename == '':
        # send error message as a flash message
        flash("No file provided", "error")
        return redirect(url_for('models'))
    
    # Ensure file is a json file
    if not is_json(file.filename):
        # send error message as a flash message
        flash("File must be a JSON file", "error")
        return redirect(url_for('models'))
    
    # Save the file to the server as a temp file
    # User's filename is not used which avoids 
    # a security breach that could come from the filename
    file.save(DATA_FOLDER + TEMP_FILENAME)

    # Attempt to load the file with UMLModel 
    # To ensure the file will work as the model
    model = UMLModel()
    try:
        status, msg = model.load_model(TEMP_FILENAME, directory=DATA_FOLDER)
    except:
        # send error message as a flash message
        flash("File cannot be interpretted as a UMLModel", "error")
        return redirect(url_for('models'))

    # load model failed
    if not status:
        flash(msg, "error")
        return redirect(url_for('models'))

    # Save file as the new working model 
    with open(DATA_FOLDER + TEMP_FILENAME, "r") as src:
        with open(DATA_FOLDER + request.form.get("model_name") + ".json", "w") as dest:
            dest.writelines(src.readlines())

    # Redirect to the homepage to display 
    # the newly loaded model
    flash("File was successfully uploaded", "success")
    return redirect(url_for('models'))
        
##########################################################################

if __name__ == '__main__':
    # run in debug mode
    # server will automatically close and restart if 
    # a source code file was changed 
    if len(sys.argv) == 2 and sys.argv[1] == '-debug':
        app.run(debug=True)
    else:
        app.run(debug=False)
