import json
import os
import datetime as datetime
import logger as log
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getPassword(config):
    '''
    Retrieve email password

    Input:
        config (dict): Configuration key value pairs
    Output:
        password (str): Gmail password for the requested platform
    '''

    log.note(config,f"Function call: getPassword")

    configs = {
        'windows':  'C:/Users/smith/LocalConfig/PersonalAssistant/email.json',
        'mac':      '/Users/smith/local_config/email.json',
        'ubuntu':   '/home/smith/Documents/Code/local_config/email.json',
        'default':  'protectedInfo.json'
    }

    config_path = ''

    for c in configs.keys():
        if os.path.exists(configs[c]):
            config_path = configs[c]
            break

    if config_path == '':
        log.note(config,f"getPassword: FAILED TO LOCATE EMAIL PASSWORD FILE")

    password = ''
    with open(config_path, 'r') as file:
        passwordInfo = json.loads(file.read())
        password = passwordInfo['gmailPassword'][config['platform']]
    
    return password

def sendEmail(config):
    '''
    Send email update

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: sendEmail")

    try:
        with open(config['messageFile'], 'r') as f:
            html = f.read()
    except Exception as e:
        log.note(config,f"sendEmail: FAILED TO RETRIEVE MESSAGE\n    Error: {e}")
    
    log.note(config,f"sendEmail: Retrieved message content")

    try:
        # Create SMTP session
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()  # Enable TLS encryption
        server.login(config['from_email'], getPassword(config))

        # Create message container
        msg = MIMEMultipart('related')
        msg['From'] = config['from_email']
        msg['To'] = config['to_email']

        if config['subject'] == "default":
            msg['Subject'] = "Daily Correspondence ({0})".format(datetime.datetime.now().strftime("%Y-%m-%d"))
        else:
            msg['Subject'] = config['subject']

        # Create the HTML part
        html_part = MIMEMultipart('alternative')
        html_mime = MIMEText(html, 'html')
        html_part.attach(html_mime)
        
        # Attach HTML part to main message
        msg.attach(html_part)
        
        # Send email
        text = msg.as_string()
        server.sendmail(config['from_email'], config['to_email'], text)
        server.quit()
        
        log.note(config,f"sendEmail: Email sent successfully!")
        return True
        
    except Exception as e:
        log.note(config,f"sendEmail: FAILED TO SEND MESSAGE\n    Error: {e}")
        return False