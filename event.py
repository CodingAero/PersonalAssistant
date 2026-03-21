from datetime import datetime
from datetime import timedelta
import json
import logger as log
import message

def eventMessage(config):
    '''
    Appends upcoming event information to the correspondence message

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: eventMessage")

    msg = []
    
    # Configuration
    projection = int(config['eventOutlook'])

    # Define today
    today = datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    # Read the JSON data from the file
    with open(config['datesFile'], "r", encoding="utf-8") as file_handle:
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
                event_date = datetime(event_year, event_month, event_day)
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
                if ((today - datetime(year_11m_out, month_11m_out, day_11m_out)).days > 0) or missing_year:
                    monthiversary = False
                    # Define reference date as upcoming day when a celebration would occur
                    reference_date = datetime(int(today.year), event_month, event_day)
                    # Account for events at the start of the following year
                    if (reference_date - today).days < 0:
                        reference_date = datetime(int(today.year)+1, event_month, event_day)
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
                            if (today - datetime(incremented_year, incremented_month, event_day)).days > 0:
                                reference_date = datetime(incremented_year, incremented_month+1, event_day)
                                month_count = i + 1
                        except:
                            # Potentially the 30th day of the month
                            try:
                                if (today - datetime(incremented_year, incremented_month, event_day-1)).days > 0:
                                    reference_date = datetime(incremented_year, incremented_month+1, event_day-1)
                                    month_count = i + 1
                            except:
                                # Potentially the 29th day of the month
                                try:
                                    if (today - datetime(incremented_year, incremented_month, event_day-2)).days > 0:
                                        reference_date = datetime(incremented_year, incremented_month+1, event_day-2)
                                        month_count = i + 1
                                except:
                                    # Potentially the 28th day of the month
                                    try:
                                        if (today - datetime(incremented_year, incremented_month, event_day-3)).days > 0:
                                            reference_date = datetime(incremented_year, incremented_month+1, event_day-3)
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
                msg.append('Today is ' + str(i))
        elif key == '1':
            for i in days_until[key]:
                # print("Tomorrow is " + str(i))
                msg.append('Tomorrow is ' + str(i))
        else:
            for i in days_until[key]:
                date = (today + timedelta(days=int(key))).strftime("%A, %B %d")
                # print("In " + str(key) + " days, on " + str(date) + ", it will be " + str(i))
                msg.append('In ' + str(key) + ' days, on ' + str(date) + ', it will be ' + str(i))

    message.appendMessage(config, 'Birthdays/Anniversaries', msg)
    
    return