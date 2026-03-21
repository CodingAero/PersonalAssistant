from datetime import date
import logger as log
import message

def taxMessage(config):
    '''
    Appends upcoming quarterly tax payment alert to the correspondence message

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: taxMessage")

    today = date.today()

    outlook = int(config['eventOutlook'])

    msg = []

    # First Quarter - April 15
    q1_days = (date(date.today().year, 4, 15) - today).days
    if q1_days <= outlook and q1_days >= 0:
        msg.append('First quarter tax payment is due on April 15. (<a href="https://tax.colorado.gov/business-income-tax-estimated-payments">CO State Taxes</a> + <a href="https://www.colorado.gov/revenueonline/_/">Payment Portal</a>)')
        log.note(config,f"taxMessage: First quarter tax payment is due on April 15.")
    # Second Quarter - June 15
    q2_days = (date(date.today().year, 6, 15) - today).days
    if q2_days <= outlook and q2_days >= 0:
        msg.append('Second quarter tax payment is due on June 15. (<a href="https://tax.colorado.gov/business-income-tax-estimated-payments">CO State Taxes</a> + <a href="https://www.colorado.gov/revenueonline/_/">Payment Portal</a>)')
        log.note(config,f"taxMessage: Second quarter tax payment is due on June 15.")
    # Third Quarter - September 15
    q3_days = (date(date.today().year, 9, 15) - today).days
    if q3_days <= outlook and q3_days >= 0:
        msg.append('Third quarter tax payment is due on September 15. (<a href="https://tax.colorado.gov/business-income-tax-estimated-payments">CO State Taxes</a> + <a href="https://www.colorado.gov/revenueonline/_/">Payment Portal</a>)')
        log.note(config,f"taxMessage: Third quarter tax payment is due on September 15.")
    # Fourth Quarter - January 15
    q4_days = (date(date.today().year, 1, 15) - today).days
    if q4_days <= outlook and q4_days >= 0:
        msg.append('Fourth quarter tax payment is due on January 15. (<a href="https://tax.colorado.gov/business-income-tax-estimated-payments">CO State Taxes</a> + <a href="https://www.colorado.gov/revenueonline/_/">Payment Portal</a>)')
        log.note(config,f"taxMessage: Fourth quarter tax payment is due on January 15.")

    message.appendMessage(config, 'Quarterly Taxes', msg)
    
    return