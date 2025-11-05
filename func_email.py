# Import statements
import datetime as datetime
import func_general as g
import func_statusLogging as sl
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

##########################################################################
# Configuration
##########################################################################

config_path = g.configPath()

with open(config_path) as file:
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

def save_html_email_to_file(html_content, filename="email_preview.html"):
    """
    Save HTML email to a file for preview (without actually sending)
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML email preview saved to {filename}")

def reportFindings(html_content,verbose):
    '''
    Send correspondence via email

    Input:
        html_content (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        n/a
    '''

    if verbose: sl.progressMessage("Starting the 'reportFindings' function.",verbose)

    subject = cnfg['subject']

    if subject == "default":
        subject = "Daily Correspondence ({0})".format(datetime.datetime.now().strftime("%Y-%m-%d"))

    save_html_email_to_file(html_content, filename="email_preview.html")

    try:
        # Create SMTP session
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()  # Enable TLS encryption
        server.login(from_email, g.get_pass(platform,verbose))

        # Create message container
        msg = MIMEMultipart('related')
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Create the HTML part
        html_part = MIMEMultipart('alternative')
        html_mime = MIMEText(html_content, 'html')
        html_part.attach(html_mime)
        
        # Attach HTML part to main message
        msg.attach(html_part)
        
        # Send email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print("Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False