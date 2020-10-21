# Flask Server for UMLEditor GUI
# Description:     
#   This file uses Flask to serve up files for out GUI 
#   This acts as our main Controller of the GUI
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 3 2020
##########################################################################
# Imports

import os
import sys
from flask import Flask, render_template, send_file, request
from flask import url_for, redirect
from werkzeug.utils import secure_filename

# Include parent directory
sys.path.append(os.getcwd())
from command.command import CommandHistory, CreateClassGUICommand
from command.command import EditClassGUICommand, DeleteClassGUICommand
from models.UMLModel import UMLModel

##########################################################################
# Globals 

app = Flask(__name__)

app.config['SECRET_KEY'] = '2ca8690a209df45699ccf028b6a47015'

# Where the data model is saved
DATA_FOLDER = os.path.join(os.getcwd(), 'data/')
# The name of the server's current working model file
WORKING_FILENAME = '__WorkingModel__.json'
TEMP_FILENAME = '__temp__.json'
HISTORY_LIMIT = 20

# keeps track of prior commands 
command_history = CommandHistory(HISTORY_LIMIT)

##########################################################################

# The home page
@app.route("/")
def dashboard():
    # Get current model
    model = UMLModel()
    model.load_model(WORKING_FILENAME)

    # Setup template data
    data = {
        "classes" : []
    }

    # add each class
    i = 0 
    for class_name in model.classes:
        data["classes"] += [model.classes[class_name].get_raw_data()]
        # Give class its index 
        data["classes"][i]["index"] = i+1
        i += 1

    return render_template("dashboard.html", data=data)

##########################################################################

# Creates a class from the given class data in POST request
@app.route("/createClass", methods=["GET", "POST"])
def createClass():
    # Ensure there was a POST request
    if request.method != "POST":
        return "Nothing in POST"

    # Grab the data from the POST request 
    # and structure it for the command
    class_data = {
        "filename" : WORKING_FILENAME,
        "class_name" : request.form.get('class_name'),
        "field_visibilities" : list(request.form.getlist('field_visibility')),
        "field_types" : list(request.form.getlist('field_type')),
        "field_names" : list(request.form.getlist('field_name')),
        "method_visibilities" : list(request.form.getlist('method_visibility')),
        "method_types" : list(request.form.getlist('method_type')),
        "method_names" : list(request.form.getlist('method_name')),
        "relationship_types" : list(request.form.getlist('relationship_type')),
        "relationship_others" : list(request.form.getlist('relationship_other'))
    }

    # create command 
    command = CreateClassGUICommand(UMLModel(), class_data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response
    if response:
        status, msg = response

        # command was successful 
        if status:
            # add to history
            command_history.push(command)

            # print success message 
            print(msg)
        
            return redirect(url_for('dashboard'))

    # command failed
    print(f"ERROR: {msg}")
    return msg

##########################################################################

# Edits an existing class
@app.route("/editClass", methods=["GET", "POST"])
def editClass():
    # Ensure there was a POST request
    if request.method != "POST":
        return "Nothing in POST"

    # Create new class with new data
    # Grab the data from the POST request 
    class_data = {
        "filename" : WORKING_FILENAME,
        "original_name" : request.form.get('original_name'),
        "class_name" : request.form.get('class_name'),
        "field_visibilities" : list(request.form.getlist('field_visibility')),
        "field_types" : list(request.form.getlist('field_type')),
        "field_names" : list(request.form.getlist('field_name')),
        "method_visibilities" : list(request.form.getlist('method_visibility')),
        "method_types" : list(request.form.getlist('method_type')),
        "method_names" : list(request.form.getlist('method_name')),
        "relationship_types" : list(request.form.getlist('relationship_type')),
        "relationship_others" : list(request.form.getlist('relationship_other'))
    }

    # create command 
    command = EditClassGUICommand(UMLModel(), class_data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response
    if response:
        status, msg = response

        # command was successful 
        if status:
            # add to history
            command_history.push(command)
        
            # print success message 
            print(msg)

            return redirect(url_for('dashboard'))

    # command failed
    print(f"ERROR: {msg}")
    return msg

##########################################################################

# Serves the contents of the modal with a given class_name
# This is for the edit modal
@app.route("/editForm", methods=['GET', 'POST'])
def editForm():
    # Ensure there was a POST request
    if request.method != "POST":
        return "Nothing in POST"
    
    # load model
    model = UMLModel()
    model.load_model(WORKING_FILENAME)

    # ensure class exists
    if request.form.get('class_name') not in model.classes:
        return f"Class '{request.form.get('class_name')}' does not exist"

    # grab class data
    data = model.classes[request.form.get('class_name')].get_raw_data()

    # Build modal form inputs
    return render_template("modalForm.html", data=data)

##########################################################################

# Server for deleting a class
@app.route("/deleteClass", methods=["GET", "POST"])
def deleteClass():

    # Ensure method was post
    if request.method != 'POST':
        return "<h1 style='text-align:center'>Nothing sent in POST</h1>"

    # Print out what is being deleted
    print (f"Deleting class '{request.form.get('class_name')}' from the model")
    
    # Grab the data from the POST request 
    class_data = {
        "filename" : WORKING_FILENAME,
        "class_name" : request.form.get('class_name')
    }
    
    # create command 
    command = DeleteClassGUICommand(UMLModel(), class_data)
    # save backup
    command.saveBackup()
    # execute command
    response = command.execute()

    # ensure response
    if response:
        status, msg = response

        # command was successful 
        if status:
            # add to history
            command_history.push(command)
        
            # print success message 
            print(msg)
            
            return redirect(url_for('dashboard'))

    # command failed
    print(f"ERROR: {msg}")
    return msg

##########################################################################

# Undoes a previously executed command
@app.route("/undo")
def undo():
    # get undoable command
    command = command_history.pop_undo()

    # ensure there was a command
    if command == None:
        return "ERROR: No command to undo"
    
    # undo the command
    command.undo()

    # Redirect user back to main page 
    return redirect(url_for('dashboard'))

##########################################################################

# redo a previously undone command
@app.route("/redo")
def redo():
    # get undone command
    command = command_history.pop_redo()

    # ensure there was a command
    if command == None:
        return "ERROR: No command to redo"
    
    # redo the command
    command.execute()

    # Redirect user back to main page 
    return redirect(url_for('dashboard'))

##########################################################################

# Server for Downloading models 
@app.route("/download")
def download():
    return send_file(DATA_FOLDER + WORKING_FILENAME)

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
        return "<h1 style='text-align:center'>Nothing sent in POST</h1>"

    # Ensure POST has a 'file' 
    if 'file' not in request.files:
        return "<h1 style='text-align:center'>No file</h1>"
    
    # Grab file
    file = request.files['file']

    # Ensure there was a file submitted
    if file.filename == '':
        return "<h1 style='text-align:center'>No file submitted</h1>"
    
    # Ensure file is a json file
    if not is_json(file.filename):
        return "<h1 style='text-align:center'>Bad File Extension</h1>"
    
    # Save the file to the server as a temp file
    # User's filename is not used which avoids 
    # a security breach that could come from the filename
    file.save(DATA_FOLDER + TEMP_FILENAME)

    # Attempt to load the file with UMLModel 
    # To ensure the file will work as the model
    model = UMLModel()
    try:
        model.load_model(TEMP_FILENAME)
    except:
        return "<h1 style='text-align:center'>Model File Not Parse-able</h1>"

    # Save file as the new working model 
    with open(DATA_FOLDER + TEMP_FILENAME, "r") as src:
        with open(DATA_FOLDER + WORKING_FILENAME, "w") as dest:
            dest.writelines(src.readlines())

    # Redirect to the homepage to display 
    # the newly loaded model
    return redirect(url_for('dashboard'))
        
##########################################################################

if __name__ == '__main__':
    # run in debug mode
    # server will automatically close and restart if 
    # a source code file was changed 
    if len(sys.argv) == 2 and sys.argv[1] == '-debug':
        app.run(debug=True)
    else:
        app.run(debug=False)
