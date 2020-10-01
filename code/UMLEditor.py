# An Editor for UML models 
# Description:     
#   This file is the entry point for either the GUI or CLI
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     September 30 2020

##########################################################################
# Imports

import sys
from WebApp import main as GUIMain
from CLI import CLIEditor

##########################################################################
# Constants 

def main():

    # No arguments - run GUI application
    if len(sys.argv) == 1:
        print ("Running WebApp version of UMLEditor")
        print ("Open a browser and go to 'localhost:5000' to see the local webpage")
        GUIMain.app.run(debug=True)
    # Argument is -cli for command line interface
    elif len(sys.argv) == 2 and sys.argv[1] == '-cli':
        print ("This is the command-line interface for UMLEditor")
        CLIEditor.REPL()
    # Too many arguments or invalid argument
    else:
        print ("Usages:")
        print (f"{sys.argv[0]}")
        print ("\t runs the Web based UML Editor")
        print (f"{sys.argv[0]} -cli")
        print ("\t runs the Command-line interface version of UML Editor")

if __name__ == "__main__":
    main()