# Flask Server for UMLEditor GUI
# Description:     
#   This file uses Flask to serve up files for out GUI 
#   This acts as our main Controller of the GUI
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 30 2020
##########################################################################

import os
from flask import Flask, render_template, send_file
app = Flask(__name__)

##########################################################################

# The home page
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

##########################################################################

# Download models server 
@app.route("/download")
def download():
    return send_file(os.path.join(os.getcwd(), 'data/tempdata.json'))

##########################################################################

if __name__ == '__main__':
    app.run(debug=True)