# An Editor for UML models 
# Description:     
#   This file is the entry point for either the GUI or CLI
# Course:   CSCI 420 - Software Engineering
# Authors:  Adisa, Amy, Carli, David, Joan
# Date:     October 3 2020

##########################################################################
# Imports

import cmd
import sys
import webbrowser
import subprocess
from CLI import CLIEditor

##########################################################################
# Constants 

##########################################################################

def main():

    # No arguments - run GUI application
    if len(sys.argv) == 1:
        print ("Running WebApp version of UMLEditor")
        # Opens up GUI application in user's default browser
        webbrowser.open('http://localhost:5000/')
        # Create subprocess to run the server
        process = subprocess.Popen(['python3', 'WebApp/main.py'])
        # Wait for the server to close
        try:
            process.wait()
        except:
            print ("Server shutting down")
    # No arguments - run GUI application
    elif len(sys.argv) == 2 and sys.argv[1] == '-debug':
        print ("Running WebApp version of UMLEditor (in debug mode)")
        # Opens up GUI application in user's default browser
        webbrowser.open('http://localhost:5000/')
        # Create subprocess to run the server
        process = subprocess.Popen(['python3', 'WebApp/main.py', '-debug'])
        # Wait for the server to close
        try:
            process.wait()
        except:
            print ("Server shutting down")
    # Argument is -cli for command line interface
    elif len(sys.argv) == 2 and sys.argv[1] == '-cli':
        CLIEditor.runCMD()
    # Too many arguments or invalid argument
    else:
        print ("Usages:")
        print (f"{sys.argv[0]}")
        print ("\t runs the Web based UML Editor")
        print (f"{sys.argv[0]} -debug")
        print ("\t runs the Web based UML Editor in debug/developer mode")
        print (f"{sys.argv[0]} -cli")
        print ("\t runs the Command-line interface version of UML Editor")

##########################################################################

if __name__ == "__main__":
    main()