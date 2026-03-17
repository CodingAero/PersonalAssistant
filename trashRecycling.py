from datetime import datetime
import logger as log
import message

def trashRecyclingMessage(config):
    '''
    Appends upcoming trash and recycling day information to the correspondence message

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: trashRecyclingMessage")

    now = datetime.now()

    msg = []
    
    if (now.isocalendar()[1] % 2) > 0: # Alternating recycling weeks
        if now.weekday() == 0: # Monday
            msg.append('Tomorrow is trash day.')
            log.note(config,f"trashRecyclingMessage: Tomorrow is trash day.")
        elif now.weekday() == 1: # Tuesday
            msg.append('It is trash day.')
            log.note(config,f"trashRecyclingMessage: It is trash day.")
    else:
        if now.weekday() == 0: # Monday
            msg.append('Tomorrow is a trash and recycling day.')
            log.note(config,f"trashRecyclingMessage: Tomorrow is a trash and recycling day.")
        elif now.weekday() == 1: # Tuesday
            msg.append('It is a trash and recycling day.')
            log.note(config,f"trashRecyclingMessage: It is a trash and recycling day.")

    message.appendMessage(config, 'Trash/Recycling', msg)
    
    return