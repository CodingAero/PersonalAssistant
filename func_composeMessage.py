# Import statements
import json
import datetime as datetime
import func_statusLogging as sl

##########################################################################
# Configuration
##########################################################################

with open('config.json', 'r') as file:
    cnfg = json.loads(file.read())
    yourName = cnfg['yourName']
    assistantName = cnfg['assistantName']
    eventOutlook = int(cnfg['eventOutlook'])

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
    
    msg = "{0},\n\n".format(yourName) + \
        "Let me catch you up on some relevant information for today."

    return str(msg)

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
    msg = (msg + '\n\n' + 'Birthdays and Anniversaries:')

    # Read the JSON data from the file
    path = r'data_dates.json'
    with open(path, "r", encoding="utf-8") as file_handle:
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
                msg = (msg + '\n' + 'Today is ' + str(i))
        elif key == '1':
            for i in days_until[key]:
                # print("Tomorrow is " + str(i))
                msg = (msg + '\n' + 'Tomorrow is ' + str(i))
        else:
            for i in days_until[key]:
                date = (today + datetime.timedelta(days=int(key))).strftime("%A, %B %d")
                # print("In " + str(key) + " days, on " + str(date) + ", it will be " + str(i))
                msg = (msg + '\n' + 'In ' + str(key) + ' days, on ' + str(date) + ', it will be ' + str(i))

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
        msg = (msg + '\n\n' + 'Credit Card:' + '\n' + 'Time to pay your credit card.')

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
            msg = (msg + '\n\n' + 'Trash/Recycling:' + '\n' + 'Tomorrow is trash day.')
        elif now.weekday() == 1: # Tuesday
            msg = (msg + '\n\n' + 'Trash/Recycling:' + '\n' + 'It is trash day.')
    else:
        if now.weekday() == 0: # Monday
            msg = (msg + '\n\n' + 'Trash/Recycling:' + '\n' + 'Tomorrow is a trash and recycling day.')
        elif now.weekday() == 1: # Tuesday
            msg = (msg + '\n\n' + 'Trash/Recycling:' + '\n' + 'It is a trash and recycling day.')

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

    msg_addition = "Sincerely, {0}\n\n".format(assistantName) + \
        "In route from {0} to {1}.\n\n".format(departure, destination) + \
        "Word of the day:\n" + \
        getWord(verbose) + "\n\n" + \
        "Quote of the day:\n" + \
        getQuote(verbose)
    msg = msg + "\n\n" + msg_addition

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

    with open('history.json', 'r') as histFile:
        hist = json.loads(histFile.read())

    lastDeparture = hist['lastDeparture']
    lastStateId = int(hist['lastStateId'])
    lastCountryId = int(hist['lastCountryId'])
    
    if lastDeparture == "state":
        departureId = lastCountryId
        hist['lastDeparture'] = "country"
        hist['lastCountryId'] = str(departureId)
    else:
        departureId = lastStateId
        hist['lastDeparture'] = "state"
        hist['lastStateId'] = str(departureId)
    
    with open('data_states.json', 'r') as stateFile:
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
            hist['lastStateId'] = str(destinationId)
            destination = "{0}, {1}".format(st["states"][destinationId]["capital"],st["states"][destinationId]["state"])
        else:
            departure = "{0}, {1}".format(st["states"][departureId]["capital"],st["states"][departureId]["state"])
            
    with open('data_countries.json', 'r') as countryFile:
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
            hist['lastCountryId'] = str(destinationId)
            destination = "{0}, {1}".format(cnrt["countries"][destinationId]["capital"],cnrt["countries"][destinationId]["short-form name"])
    
    with open('history.json', 'w') as histFile:
        json.dump(hist, histFile, indent=4)
    
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

    with open('history.json', 'r') as histFile:
        hist = json.loads(histFile.read())

    lastWordId = int(hist['lastWordId'])
            
    with open('data_words.json', 'r') as wordsFile:
        wrd = json.loads(wordsFile.read())

        searching = True
        wordId = lastWordId + 1
        while searching:
            while wordId >= len(wrd["words"]):
                wordId -= len(wrd["words"])
            if wrd["words"][wordId]["skip"] == "no":
                searching = False
            else:
                wordId += 1
        hist['lastWordId'] = str(wordId)
        wotd = "{0} ({1}): {2}\nSentence: \"{3}\"".format(wrd["words"][wordId]["word"],wrd["words"][wordId]["part of speech"],wrd["words"][wordId]["definition"],wrd["words"][wordId]["sentence"])
    
    with open('history.json', 'w') as histFile:
        json.dump(hist, histFile, indent=4)
    
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

    with open('history.json', 'r') as histFile:
        hist = json.loads(histFile.read())

    lastQuoteId = int(hist['lastQuoteId'])
            
    with open('data_quotes.json', 'r') as quotesFile:
        qt = json.loads(quotesFile.read())

        searching = True
        quoteId = lastQuoteId + 1
        while searching:
            while quoteId >= len(qt["quotes"]):
                quoteId -= len(qt["quotes"])
            if qt["quotes"][quoteId]["skip"] == "no":
                searching = False
            else:
                quoteId += 1
        hist['lastQuoteId'] = str(quoteId)
        qotd = "{0} ({1})".format(qt["quotes"][quoteId]["quote"],qt["quotes"][quoteId]["author"])
    
    with open('history.json', 'w') as histFile:
        json.dump(hist, histFile, indent=4)
    
    return qotd