# Import statements
import datetime as datetime
import func_general as g
import func_statusLogging as sl
import json
import requests

##########################################################################
# Configuration
##########################################################################

config_path = g.configPath()

with open(config_path) as file:
    cnfg = json.loads(file.read())
    greeting = cnfg['greeting']
    assistantName = cnfg['assistantName']
    eventOutlook = int(cnfg['eventOutlook'])
    countriesFile = cnfg['countriesFile']
    datesFile = cnfg['datesFile']
    quotesFile = cnfg['quotesFile']
    statesFile = cnfg['statesFile']
    wordsFile = cnfg['wordsFile']

##########################################################################
# Functions
##########################################################################

def intializeMessage(verbose):
    '''
    Starts the correspondence message string

    Input:
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'intializeMessage' function.",verbose)
    
    # msg = "{0},\n\n".format(greeting) + \
    #     "Here is what you need to know."

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
                </td>
        </table>
        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 10px 10px 10px 20px;">
            <tr>
                <td>
                    <p>
                        ''' + str(greeting) + ''',
                    </p>
                    <p>
                        Here is what you need to know.
                    </p>'''

    return str(msg)

def get_weather():
    """
    Get weather from National Weather Service (US only)
    Free, no API key needed
    """
    # Get the forecast office and grid coordinates
    point_url = f"https://api.weather.gov/points/40.0379,-105.0528"
    headers = {
        "User-Agent": "WeatherApp",
        "Accept": "application/json"
        }
    
    point_response = requests.get(point_url, headers=headers)
    point_data = point_response.json()
    
    # Get the forecast URL
    forecast_url = point_data['properties']['forecast']
    
    forecast_response = requests.get(forecast_url, headers=headers)
    forecast_data = forecast_response.json()
    
    # Today's forecast
    today = forecast_data['properties']['periods'][0]

    return(today['detailedForecast'])

def weatherMessage(msg,verbose):
    '''
    Appends a weather forecast to the correspondence message

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'weatherMessage' function.",verbose)

    now = datetime.datetime.now()
    begin_alert = 5 # Day of the month, inclusive
    end_alert = 12 # Day of the month, inclusive
    
    if (int(now.strftime("%d")) >= begin_alert) and (int(now.strftime("%d")) <= end_alert):
        msg = msg + '''
                    <h2>Weather</h2>
                        <p>
                            ''' + str(get_weather()) + '''
                        </p>'''

    return msg

def creditCardMessage(msg,verbose):
    '''
    Appends upcoming credit card due date information to the correspondence message

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'creditCardMessage' function.",verbose)

    now = datetime.datetime.now()
    begin_alert = 5 # Day of the month, inclusive
    end_alert = 12 # Day of the month, inclusive
    
    if (int(now.strftime("%d")) >= begin_alert) and (int(now.strftime("%d")) <= end_alert):
        msg = msg + '''
                    <h2>Credit Card</h2>
                        <p>
                            Time to pay your credit card.
                        </p>'''

    return msg

def trashRecyclingMessage(msg,verbose):
    '''
    Appends upcoming trash and recycling day information to the correspondence message

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'trashRecyclingMessage' function.",verbose)

    now = datetime.datetime.now()
    
    if (now.isocalendar()[1] % 2) > 0: # Alternating recycling weeks
        if now.weekday() == 0: # Monday
            msg = msg + '''
                    <h2>Trash/Recycling</h2>
                        <p>
                            Tomorrow is trash day.
                        </p>'''
        elif now.weekday() == 1: # Tuesday
            msg = msg + '''
                    <h2>Trash/Recycling</h2>
                        <p>
                            It is trash day.
                        </p>'''
    else:
        if now.weekday() == 0: # Monday
            msg = msg + '''
                    <h2>Trash/Recycling</h2>
                        <p>
                            Tomorrow is a trash and recycling day.
                        </p>'''
        elif now.weekday() == 1: # Tuesday
            msg = msg + '''
                    <h2>Trash/Recycling</h2>
                        <p>
                            It is a trash and recycling day.
                        </p>'''

    return msg

def eventMessage(msg,verbose):
    '''
    Appends upcoming event information to the correspondence message

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'eventMessage' function.",verbose)
    
    # Configuration
    projection = eventOutlook

    # Define today
    today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    # Add to message
    msg = msg + '''
                    <h2>Birthdays/Anniversaries</h2>
                        <p>
                            <ul>'''

    # Read the JSON data from the file
    with open(datesFile, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    # Create an empty dictionary for days until celebration
    days_until = {}
    for i in range(projection + 1):
        days_until[str(i)] = []

    # For each date entry
    for event in data['data']:
        # Skip the entry if skip is 'yes'
        if event['skip'] == "no":
            # For entries with enough information (must include a month)
            if (event['month'] != ""):
                event_month = int(event['month'])
                # Events missing a 'day' have the day default to 1 and the message will indicate an unknown day
                if (event['day'] != ""):
                    event_day = int(event['day'])
                    missing_day = False
                else:
                    event_day = int(1)
                    missing_day = True
                # Events missing a 'year' do not display
                if (event['year'] != ""):
                    event_year = int(event['year'])
                    missing_year = False
                else:
                    event_year = int(today.year)
                    missing_year = True
                # Define event date as day of the birthday or anniversary
                event_date = datetime.datetime(event_year, event_month, event_day)
                # This event should celebrate anniversaries
                if event_month != 1:
                    year_11m_out = event_year + 1
                    month_11m_out = event_month - 1
                    if event_day > 28:
                        day_11m_out = 28
                    else:
                        day_11m_out = event_day
                else:
                    year_11m_out = event_year
                    month_11m_out = 12
                    if event_day > 28:
                        day_11m_out = 28
                    else:
                        day_11m_out = event_day
                if ((today - datetime.datetime(year_11m_out, month_11m_out, day_11m_out)).days > 0) or missing_year:
                    monthiversary = False
                    # Define reference date as upcoming day when a celebration would occur
                    reference_date = datetime.datetime(int(today.year), event_month, event_day)
                    # Account for events at the start of the following year
                    if (reference_date - today).days < 0:
                        reference_date = datetime.datetime(int(today.year)+1, event_month, event_day)
                # This event should celebrate monthiversaries
                else:
                    monthiversary = True
                    for i in range(12):
                        incremented_month = event_month + i
                        incremented_year = event_year
                        if incremented_month > 12:
                            incremented_month -= 12
                            incremented_year += 1
                        # Potentially the 31st day of the month
                        try:
                            if (today - datetime.datetime(incremented_year, incremented_month, event_day)).days > 0:
                                reference_date = datetime.datetime(incremented_year, incremented_month+1, event_day)
                                month_count = i + 1
                        except:
                            # Potentially the 30th day of the month
                            try:
                                if (today - datetime.datetime(incremented_year, incremented_month, event_day-1)).days > 0:
                                    reference_date = datetime.datetime(incremented_year, incremented_month+1, event_day-1)
                                    month_count = i + 1
                            except:
                                # Potentially the 29th day of the month
                                try:
                                    if (today - datetime.datetime(incremented_year, incremented_month, event_day-2)).days > 0:
                                        reference_date = datetime.datetime(incremented_year, incremented_month+1, event_day-2)
                                        month_count = i + 1
                                except:
                                    # Potentially the 28th day of the month
                                    try:
                                        if (today - datetime.datetime(incremented_year, incremented_month, event_day-3)).days > 0:
                                            reference_date = datetime.datetime(incremented_year, incremented_month+1, event_day-3)
                                            month_count = i + 1
                                    except:
                                        print('Error: Having some trouble resolving the monthiversary.')
                    
                days_remaining = (reference_date - today).days
                if days_remaining <= projection:
                    years = reference_date.year - event_date.year
                    # Directly appending did not work for a dictionary so we rebuild entry
                    temp_list = []
                    for e in days_until[str(days_remaining)]:
                        temp_list.append(e)
                    new_event = str(event['name']) + "."
                    if missing_year == False and not monthiversary:
                        new_event += " (" + str(years) + ")"
                    if monthiversary:
                        new_event += " (" + str(month_count) + " months)"
                    if missing_day == True:
                        new_event += " [Exact day is unknown]"
                    temp_list.append(new_event)
                    days_until[str(days_remaining)] = temp_list

    for key in days_until:
        if key == '0':
            for i in days_until[key]:
                # print("Today is " + str(i))
                msg = msg + '''
                            <li>Today is ''' + str(i) + '''</li>'''
        elif key == '1':
            for i in days_until[key]:
                # print("Tomorrow is " + str(i))
                msg = msg + '''
                            <li>Tomorrow is ''' + str(i) + '''</li>'''
        else:
            for i in days_until[key]:
                date = (today + datetime.timedelta(days=int(key))).strftime("%A, %B %d")
                # print("In " + str(key) + " days, on " + str(date) + ", it will be " + str(i))
                msg = msg + '''
                            <li>In ''' + str(key) + ''' days, on ''' + str(date) + ''', it will be ''' + str(i) + '''</li>'''

    msg = msg + '''
                        </ul>
                    </p>'''

    return msg

def wordMessage(msg,verbose):
    '''
    Add word of the day

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'wordMessage' function.",verbose)

    msg = msg + '''
                    <h2>Word of the Day</h2>
                        <p>
                            ''' + getWord(verbose) + '''
                        </p>'''

    return msg

def quoteMessage(msg,verbose):
    '''
    Add quote of the day

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'quoteMessage' function.",verbose)
    
    msg = msg + '''
                    <h2>Quote of the Day</h2>
                        <p>
                            ''' + getQuote(verbose) + '''
                        </p>'''

    return msg

def valedictionMessage(msg,verbose):
    '''
    Closes the correspondence message

    Input:
        msg (str): Text forming the body of the email correspondence
        verbose (bool): Print additional terminal messages
    Output:
        msg (str): Text forming the body of the email correspondence
    '''

    if verbose: sl.progressMessage("Starting the 'valedictionMessage' function.",verbose)

    departure,destination = getStateCountry(verbose)

    msg = msg + '''
                </td>
            </tr>
        </table>
        <table role="presentation" width="100%">
            <tr>
                <td bgcolor="#67b57e" align="center" style="color: black;">
                    <p>
                        Winston
                    </p>
                    <p>
                        In route from ''' + str(departure) + ''' to ''' + str(destination) + '''.
                    </p>
                </td>
        </table>
    </div>
    </body>
</html>'''

    return msg

def getStateCountry(verbose):
    '''
    Provide fake travel information to reinforce geography knowledge. The previous
    day's destination becomes the current days departure location.

    Input:
        verbose (bool): Print additional terminal messages
    Output:
        departure (str): State/Country and capital text to list in valediction
        destination (str): State/Country and capital text to list in valediction
    '''

    if verbose: sl.progressMessage("Starting the 'getStateCountry' function.",verbose)

    departure = ""
    destination = ""

    with open(config_path) as confFile:
        conf = json.loads(confFile.read())

    lastDeparture = conf['lastDeparture']
    lastStateId = int(conf['lastStateId'])
    lastCountryId = int(conf['lastCountryId'])
    
    if lastDeparture == "state":
        departureId = lastCountryId
        conf['lastDeparture'] = "country"
        conf['lastCountryId'] = str(departureId)
    else:
        departureId = lastStateId
        conf['lastDeparture'] = "state"
        conf['lastStateId'] = str(departureId)
    
    with open(statesFile) as stateFile:
        st = json.loads(stateFile.read())
        if lastDeparture == "state":
            searching = True
            destinationId = lastStateId + 1
            while searching:
                while destinationId >= len(st["states"]):
                    destinationId -= len(st["states"])
                if st["states"][destinationId]["skip"] == "no":
                    searching = False
                else:
                    destinationId += 1
            conf['lastStateId'] = str(destinationId)
            destination = "{0}, {1}".format(st["states"][destinationId]["capital"],st["states"][destinationId]["state"])
        else:
            departure = "{0}, {1}".format(st["states"][departureId]["capital"],st["states"][departureId]["state"])
            
    with open(countriesFile) as countryFile:
        cnrt = json.loads(countryFile.read())
        if lastDeparture == "state":
            departure = "{0}, {1}".format(cnrt["countries"][departureId]["capital"],cnrt["countries"][departureId]["short-form name"])
        else:
            searching = True
            destinationId = lastCountryId + 1
            while searching:
                while destinationId >= len(cnrt["countries"]):
                    destinationId -= len(cnrt["countries"])
                if cnrt["countries"][destinationId]["skip"] == "no":
                    searching = False
                else:
                    destinationId += 1
            conf['lastCountryId'] = str(destinationId)
            destination = "{0}, {1}".format(cnrt["countries"][destinationId]["capital"],cnrt["countries"][destinationId]["short-form name"])
    
    with open(config_path, 'w') as confFile:
        json.dump(conf, confFile, indent=4)
    
    return departure,destination

def getWord(verbose):
    '''
    Determines the next word of the day and provides a string to place
    into the daily correspondence email.

    Input:
        verbose (bool): Print additional terminal messages
    Output:
        wotd (str): Word of the day text
    '''

    if verbose: sl.progressMessage("Starting the 'getWord' function.",verbose)

    wotd = ""

    with open(config_path) as confFile:
        conf = json.loads(confFile.read())

    lastWordId = int(conf['lastWordId'])
            
    with open(wordsFile) as wrdFile:
        wrd = json.loads(wrdFile.read())

        searching = True
        wordId = lastWordId + 1
        while searching:
            while wordId >= len(wrd["words"]):
                wordId -= len(wrd["words"])
            if wrd["words"][wordId]["skip"] == "no":
                searching = False
            else:
                wordId += 1
        conf['lastWordId'] = str(wordId)
        wotd = "{0} ({1}): {2}<br>Sentence: \"{3}\"".format(wrd["words"][wordId]["word"],wrd["words"][wordId]["part of speech"],wrd["words"][wordId]["definition"],wrd["words"][wordId]["sentence"])
    
    with open(config_path, 'w') as confFile:
        json.dump(conf, confFile, indent=4)
    
    return wotd

def getQuote(verbose):
    '''
    Determines the next quote of the day and provides a string to place
    into the daily correspondence email.

    Input:
        verbose (bool): Print additional terminal messages
    Output:
        qotd (str): Quote of the day text
    '''

    if verbose: sl.progressMessage("Starting the 'getQuote' function.",verbose)

    qotd = ""

    with open(config_path) as confFile:
        conf = json.loads(confFile.read())

    lastQuoteId = int(conf['lastQuoteId'])
            
    with open(quotesFile) as qtFile:
        qt = json.loads(qtFile.read())

        searching = True
        quoteId = lastQuoteId + 1
        while searching:
            while quoteId >= len(qt["quotes"]):
                quoteId -= len(qt["quotes"])
            if qt["quotes"][quoteId]["skip"] == "no":
                searching = False
            else:
                quoteId += 1
        conf['lastQuoteId'] = str(quoteId)
        qotd = "{0}<br>~{1}".format(qt["quotes"][quoteId]["quote"],qt["quotes"][quoteId]["author"])
    
    with open(config_path, 'w') as confFile:
        json.dump(conf, confFile, indent=4)
    
    return qotd