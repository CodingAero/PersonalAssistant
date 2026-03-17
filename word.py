import json
import logger as log
import message

def wordMessage(config):
    '''
    Determines the next word of the day and provides a string
    to place into the daily correspondence email.

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: wordMessage")

    msg = []

    with open(config['configPath']) as confFile:
        conf = json.loads(confFile.read())

    lastWordId = int(conf['lastWordId'])
            
    with open(config['wordsFile']) as wrdFile:
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
        msg.append("{0} ({1}): {2}<br>Sentence: \"{3}\"".format(wrd["words"][wordId]["word"],wrd["words"][wordId]["part of speech"],wrd["words"][wordId]["definition"],wrd["words"][wordId]["sentence"]))
    
    with open(config['configPath'], 'w') as confFile:
        json.dump(conf, confFile, indent=4)

    message.appendMessage(config, 'Word of the Day', msg)

    return