##########################################################################
# Description:
#       This file is meant to provide a daily email in order to stay 
#       informed on various topics such as weather and events.
##########################################################################

import creditcard as credit
import event
import github as gh
import logger as log
import message
import quote
import sendEmail as email
import startup as start
import trashRecycling as trash
import weather
import word

from datetime import datetime

def main():
    # Log the start time of the program
    start_time = datetime.now()

    # Get the configuration items
    config = start.get_config()

    #Initialize log file
    log.intializeLog(config)

    # Determine temperature information for the message header
    current_temp,high_temp,low_temp = weather.getTemperatures(config)

    # Initialize the correspondence message
    message.intializeMessage(config,current_temp,high_temp,low_temp)

    # Expand the correspondence message
    try:
        weather.forecastMessage(config)
        credit.creditcardMessage(config)
        trash.trashRecyclingMessage(config)
        event.eventMessage(config)
        word.wordMessage(config)
        quote.quoteMessage(config)
    except Exception as e:
        log.note(config,f"FAILED TO EXPAND MESSAGE\n    Error: {e}")

    # Close the correspondence message
    message.closeMessage(config)

    # Send email
    email.sendEmail(config)

    # Log final execution time
    end_time = datetime.now()
    execution_time = end_time - start_time
    log.note(config,f"Successful program execution in {0} second(s).".format(execution_time.total_seconds()))
    print("Program completed successfully.")

    # Attempt to push log to GitHub
    try:
        gh.githubLog(config)
    except Exception as e:
        log.note(config,f"FAILED TO LOG ON GITHUB\n    Error: {e}")

if __name__ == "__main__":
    main()