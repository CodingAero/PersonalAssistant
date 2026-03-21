import datetime as datetime
import logger as log

def intializeMessage(config, current_temp='---', high_temp='---', low_temp='---'):
    '''
    Starts the correspondence message string

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: intializeMessage")

    msg = '''
        <!DOCTYPE html>
        <html>
        <head>
        <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Jura">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
        h1{font-size:40px}
        h2{font-size:20px;font-weight:600;text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1px}
        p{font-size:16px;font-weight:100}
        td{vertical-align:top}
        ul{list-style-type:square;list-style-position:outside;padding-left:10px}
        ul li{font-size:16px;font-weight:100}
        #email{margin:auto;width:600px;background-color: ghostwhite}
        </style>
        </head>
        <body bgcolor="black" style="width: 100%; font-family:Jura; font-size:18px;">
        <div id="email">
        <table role="presentation" width="100%">
        <tr>
        <td bgcolor="#67b57e" align="center" style="color: black;">
        <h1>''' + str(datetime.datetime.now().strftime("%A")) + '''</h1>
        <p>''' + str(datetime.datetime.now().strftime("%B %d, %Y")) + '''</p>
        <p>''' + str(current_temp) + '''°F (High: ''' + str(high_temp) + '''°F - Low: ''' + str(low_temp) + '''°F)</p>
        </td>
        </tr>
        </table>
        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 10px 10px 10px 20px;">
        <tr>
        <td>
        <p>
        ''' + str(config['greeting']) + ''',
        </p>
        <p>
        Here is what you need to know.
        </p>'''
    
    try:
        with open(config['messageFile'], 'w') as f:
            f.write(msg)
    except Exception as e:
        log.note(config,f"intializeMessage: FAILED TO INITIALIZE MESSAGE\n    Error: {e}")

    return

def appendMessage(config, header, body):
    '''
    Append content to the correspondence message string

    Input:
        config (dict): Configuration key value pairs
        header (str): The header for the message section
        body (list): The main content for the message section
    Output:
        n/a
    '''

    log.note(config,f"Function call: appendMessage")

    # No content to append
    if len(body) == 0:
        log.note(config,f"appendMessage: No content to append")
        return
    
    else:
        message = '''
            <h2>''' + header + '''</h2>'''
        
        # Header and paragraph
        if len(body) == 1:
            message += '''
                <p>''' + body[0] + '''</p>'''
        
        # Header and bullet points
        else:
            message += '''
                <ul>'''
            for item in body:
                message += '''
                <li>''' + item + '''</li>'''
            message += '''
                </ul>'''
    
    try:
        with open(config['messageFile'], 'a') as f:
            f.write(message)
    except Exception as e:
        log.note(config,f"appendMessage: FAILED TO APPEND MESSAGE\n    Error: {e}")

    return

def closeMessage(config):
    '''
    Close the correspondence message string

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: closeMessage")

    msg = '''
        </td>
        </tr>
        </table>
        <table role="presentation" width="100%">
        <tr>
        <td bgcolor="#67b57e" align="center" style="color: black;">
        <p>
        Winston
        </p>
        </td>
        </tr>
        </table>
        </div>
        </body>
        </html>'''
    
    try:
        with open(config['messageFile'], 'a') as f:
            f.write(msg)
    except Exception as e:
        log.note(config,f"closeMessage: FAILED TO CLOSE MESSAGE\n    Error: {e}")

    return