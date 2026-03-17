import json
import logger as log
import message

def quoteMessage(config):
    '''
    Determines the next quote of the day and provides a string
    to place into the daily correspondence email.

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: quoteMessage")

    msg = []

    with open(config['configPath']) as confFile:
        conf = json.loads(confFile.read())

    lastQuoteId = int(conf['lastQuoteId'])
            
    with open(config['quotesFile']) as qtFile:
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
        msg.append("{0}<br>~{1}".format(qt["quotes"][quoteId]["quote"],qt["quotes"][quoteId]["author"]))
    
    with open(config['configPath'], 'w') as confFile:
        json.dump(conf, confFile, indent=4)

    message.appendMessage(config, 'Quote of the Day', msg)
    
    return