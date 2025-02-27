# Import statements
import json
import func_statusLogging as sl

##########################################################################
# Configuration
##########################################################################

with open('config.json', 'r') as file:
    cnfg = json.loads(file.read())
    assistantName = cnfg['assistantName']

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
    
    msg = "Good morning Mike,\n\n" + \
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