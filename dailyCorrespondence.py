##########################################################################
# File: dailyCorrespondence.py
# Brief description: This file is meant to provide a daily email
#       in order to stay informed on various topics.
# Author: Michael J. Smith
# Created: July 06, 2022
##########################################################################

# Import statements
import func_composeMessage as cm
import func_email as em
import func_statusLogging as sl
import json
from datetime import datetime

##########################################################################
# Configuration
##########################################################################

# Note: Find the configuration items in config.json
with open('config.json', 'r') as file:
    cnfg = json.loads(file.read())

    # Specify the platform from which the script is being run.
    # Gmail access requires the use of an 'App Password'
    # Passwords have been generated for the following platforms:
    # 'iPhone','iPad','Mac','WindowsPhone','WindowsComp','Rasp'
    platform  = cnfg['platform']

    # Toggle to True if you prefer the email is printed within the terminal
    # window rather than being sent as an actual email.
    emailInTerminal = cnfg['emailInTerminal'] == "True" # Bool conversion

    # Toggle print messages
    verbose = cnfg['verbose'] == "True" # Bool conversion

    # File path to the log file
    logFile = cnfg['logFile']

    # This specifies how the assistant will refer to theirself
    assistantName = cnfg['assistantName']

##########################################################################
# Program logic
##########################################################################

start_time = datetime.now()

#Initialize log file
sl.intializeLog()

# Initialize the correspondence message
msg = cm.intializeMessage(verbose)

# Expand the correspondence message
msg = cm.eventMessage(msg, verbose)
msg = cm.creditCardMessage(msg, verbose)
msg = cm.trashRecyclingMessage(msg, verbose)

# Clos the correspondence message
msg = cm.valedictionMessage(msg, verbose)

# Print email in terminal vs send email
sl.infoMessage("Final correspondence message\n{0}".format(msg),verbose)
if emailInTerminal:
    print(msg)
else:
    em.reportFindings(msg, verbose)

# Print a final message to screen
end_time = datetime.now()
execution_time = end_time - start_time
sl.infoMessage("Successful program execution in {0} second(s).".format(execution_time.total_seconds()),verbose)