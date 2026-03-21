from datetime import date
import logger as log
import message

def skylightMessage(config):
    '''
    Appends reminder to upload Skylight pictures to the correspondence message

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: skylightMessage")

    today = date.today()

    msg = []

    if today.day in [1,2,3]:
        msg.append('Upload favorite pictures to Skylight.')
        log.note(config,f"skylightMessage: Upload favorite pictures to Skylight.")

    message.appendMessage(config, 'Skylight Pictures', msg)
    
    return