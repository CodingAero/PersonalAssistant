# Import statements
import func_general as g
import json
from datetime import datetime

##########################################################################
# Configuration
##########################################################################

config_path = g.configPath()

with open(config_path) as file:
    cnfg = json.loads(file.read())
    logFile = cnfg['logFile']

##########################################################################
# Functions
##########################################################################

def intializeLog():
    """
    Creates a new log file or clears the contents of the existing log file.
    
    Input:
        n/a
    Output:
        n/a
    """

    try:
        with open(logFile, 'w') as f:
            f.write("Program initialized: {0}".format(datetime.now()))
    except Exception as e:
        errorMessage(f"An error occurred initializing the log file: {e}",verbose=True)
    
    return

def errorMessage(txt,verbose):
    '''
    Prints an Error message in the log file

    Input:
        msg (str): Error message text
        verbose (bool): Print additional terminal messages
    Output:
        n/a
    '''

    if verbose: print("\nERROR: {0}".format(txt))

    with open(logFile, 'a') as f:
        f.write("\nERROR: {0}".format(txt))

    return

def infoMessage(txt,verbose):
    '''
    Prints an Info message in the log file

    Input:
        txt (str): Info message text
        verbose (bool): Print additional terminal messages
    Output:
        n/a
    '''

    try:
        with open(logFile, 'a') as f:
            f.write("\nINFO: {0}".format(txt))
    except Exception as e:
        errorMessage(f"An error occurred logging an info message: {e}")
    
    return

def progressMessage(txt,verbose):
    '''
    Prints an Info message in the log file

    Input:
        txt (str): Info message text
        verbose (bool): Print additional terminal messages
    Output:
        n/a
    '''

    if verbose:
        try:
            with open(logFile, 'a') as f:
                f.write("\nProgress: {0}".format(txt))
        except Exception as e:
            errorMessage(f"An error occurred logging a progress message: {e}")
    
    return