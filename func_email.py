# Import statements
import json
import smtplib
import datetime as datetime
import func_statusLogging as sl

##########################################################################
# Configuration
##########################################################################

with open('config.json', 'r') as file:
    cnfg = json.loads(file.read())
    platform = cnfg['platform']
    emailInTerminal = cnfg['emailInTerminal'] == "True" # Bool conversion
    verbose = cnfg['verbose'] == "True" # Bool conversion
    logFile = cnfg['logFile']
    assistantName = cnfg['assistantName']
    from_email = cnfg['from_email']
    to_email = cnfg['to_email']
    subject = cnfg['subject']

##########################################################################
# Functions
##########################################################################

def reportFindings(msg,verbose):
    '''
    Send correspondence via email

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        n/a
    '''

    if verbose: sl.progressMessage("Starting the 'reportFindings' function.",verbose)

    subject = cnfg['subject']

    if subject == "default":
        subject = "Daily Correspondence ({0})".format(datetime.datetime.now().strftime("%Y-%m-%d"))

    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(from_email,get_pass(platform,verbose))
    header = "To: " + to_email + "\nFrom: " + from_email
    header = header + "\nSubject: " + subject + "\n"
    URGENT_MESSAGE = header + "\n" + msg
    smtpserver.sendmail(from_email,to_email,URGENT_MESSAGE)
    smtpserver.close()

    return

def get_pass(platform,verbose):
    '''
    Send correspondence via email

    Input:
        platform (str): Platform the program is running on
        verbose (bool): Print additional terminal messages
    Output:
        pw (str): Gmail password for the requested platform
    '''

    if verbose: sl.progressMessage("Starting the 'get_pass' function.",verbose)

    pw = ''
    with open('protectedInfo.json', 'r') as file:
        pInfo = json.loads(file.read())
        pw = pInfo['gmailPassword'][platform]
    return pw