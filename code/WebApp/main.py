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
from flask import url_for, redirect, flash
from werkzeug.utils import secure_filename

# Include parent directory
sys.path.append(os.getcwd())
from command.command import CommandHistory, CreateClassGUICommand
from command.command import EditClassGUICommand, DeleteClassGUICommand, SetClassPositonGUICommand
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
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard'))

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
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard'))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard'))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard'))

##########################################################################

# Edits an existing class
@app.route("/editClass", methods=["GET", "POST"])
def editClass():
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard'))

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

    # ensure response - this occurs if someone forgot to return a status from a command
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard'))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard'))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard'))

##########################################################################

# Serves the contents of the modal with a given class_name
# This is for the edit modal
@app.route("/editForm", methods=['GET', 'POST'])
def editForm():
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard'))
    
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

# Saves the position of a class card based on its location on the dashboard
@app.route("/saveCardPosition", methods=['POST'])
def saveCardPosition():
    # Ensure there was a POST request
    if request.method != "POST":
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard'))

    # load model
    model = UMLModel()
    model.load_model(WORKING_FILENAME)

    # Grab the position data from the POST request 
    class_data = {
        "filename" : WORKING_FILENAME,
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
        return redirect(url_for('dashboard'))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard'))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard'))


##########################################################################

# Server for deleting a class
@app.route("/deleteClass", methods=["GET", "POST"])
def deleteClass():

    # Ensure method was post
    if request.method != 'POST':
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard'))

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
    if not response:
        print(f"ERROR: Command did not give a status")
        # send error message as a flash message
        flash("Command did not give a status; This is most likely due to a bug", "error")
        return redirect(url_for('dashboard'))

    status, msg = response

    # command was not successful 
    if not status:
        # command failed
        print(f"ERROR: {msg}")
        # send error message as a flash message
        flash(msg, "error")
        return redirect(url_for('dashboard'))

    # add to history
    command_history.push(command)

    # send success message as a flash message
    print(f"SUCCESS: {msg}")
    flash(msg, "success")
    return redirect(url_for('dashboard'))


##########################################################################

# Undoes a previously executed command
@app.route("/undo")
def undo():
    # get undoable command
    command = command_history.pop_undo()

    # ensure there was a command
    if command == None:
        # send error message as a flash message
        flash("Nothing to undo", "error")
        return redirect(url_for('dashboard'))
    
    # undo the command
    command.undo()

    # send success message as a flash message
    print(f"SUCCESS: Successfully undid last command")
    flash("Undo successful", "success")
    return redirect(url_for('dashboard'))

##########################################################################

# redo a previously undone command
@app.route("/redo")
def redo():
    # get undone command
    command = command_history.pop_redo()

    # ensure there was a command
    if command == None:
        # send error message as a flash message
        flash("Nothing to redo", "error")
        return redirect(url_for('dashboard'))
    
    # redo the command
    command.execute()

    # send success message as a flash message
    print(f"SUCCESS: Redo successful")
    flash("Redo successful", "success")
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
        # send error message as a flash message
        flash("Nothing sent in POST", "error")
        return redirect(url_for('dashboard'))

    # Ensure POST has a 'file' 
    if 'file' not in request.files:
        # send error message as a flash message
        flash("No file provided", "error")
        return redirect(url_for('dashboard'))
    
    # Grab file
    file = request.files['file']

    # Ensure there was a file submitted
    if file.filename == '':
        # send error message as a flash message
        flash("No file provided", "error")
        return redirect(url_for('dashboard'))
    
    # Ensure file is a json file
    if not is_json(file.filename):
        # send error message as a flash message
        flash("File must be a JSON file", "error")
        return redirect(url_for('dashboard'))
    
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
        # send error message as a flash message
        flash("File cannot be interpretted as a UMLModel", "error")
        return redirect(url_for('dashboard'))

    # Save file as the new working model 
    with open(DATA_FOLDER + TEMP_FILENAME, "r") as src:
        with open(DATA_FOLDER + WORKING_FILENAME, "w") as dest:
            dest.writelines(src.readlines())

    # Redirect to the homepage to display 
    # the newly loaded model
    flash("File was successfully loaded", "success")
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
