# Flask Server for UMLEditor GUI
# Description:     
#   This file uses Flask to serve up files for out GUI 
#   This acts as our main Controller of the GUI
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 2 2020
##########################################################################
# Imports

import os
from flask import Flask, render_template, send_file, request
from flask import url_for, redirect
from models.UMLModel import UMLModel
from werkzeug.utils import secure_filename

##########################################################################
# Globals 

app = Flask(__name__)

app.config['SECRET_KEY'] = '2ca8690a209df45699ccf028b6a47015'

# Where the data model is saved
DATA_FOLDER = os.path.join(os.getcwd(), 'data/')
# The name of the server's current working model file
WORKING_FILENAME = '__WorkingModel__.json'
TEMP_FILENAME = '__temp__.json'

##########################################################################

# The home page
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

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
    app.run(debug=True)
