import datetime as datetime
import logger as log
import message

def creditcardMessage(config):
    '''
    Appends upcoming credit card due date information to the correspondence message

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: creditcardMessage")

    msg = []

    now = datetime.datetime.now()
    begin_alert = 5 # Day of the month, inclusive
    end_alert = 12 # Day of the month, inclusive
    
    if (int(now.strftime("%d")) >= begin_alert) and (int(now.strftime("%d")) <= end_alert):
        msg.append('Time to pay your credit card.')
        log.note(config,f"creditcardMessage: Time to pay your credit card.")

    message.appendMessage(config, 'Credit Card', msg)
    
    return