import json
import os

def configPath(verbose=False):
    '''
    Provide the configuration file path to keep real data out of the github
    repository and prevent constant updates for various environments.

    Input:
        n/a
    Output:
        config_path (str): File path to the configuration file
    '''

    configs = {
        'mac':      '/Users/smith/local_config/personal_assistant.json',
        'ubuntu':   '/home/smith/Documents/Code/local_config/personal_assistant/personal_assistant.json',
        'default':  'config.json'
    }

    config_path = ''

    for c in configs.keys():
        if os.path.exists(configs[c]):
            config_path = configs[c]
            if verbose: print("\n\n* Using '{0}' config\n\n".format(str(c)))
            break

    if config_path == '':
        if verbose: print("Unable to locate a file containing your configuration.")
        exit()

    return config_path

def get_pass(platform,verbose):
    '''
    Send correspondence via email

    Input:
        platform (str): Platform the program is running on
        verbose (bool): Print additional terminal messages
    Output:
        pw (str): Gmail password for the requested platform
    '''

    if verbose: sl.progressMessage("Starting the 'get_pass' function.",verbose)

    configs = {
        'mac':      '/Users/smith/local_config/email.json',
        'ubuntu':   '/home/smith/Documents/Code/local_config/email.json',
        'default':  'protectedInfo.json'
    }

    config_path = ''

    for c in configs.keys():
        if os.path.exists(configs[c]):
            config_path = configs[c]
            break

    if config_path == '':
        if verbose: print("Unable to locate a file containing your email password.")
        exit()

    pw = ''
    with open(config_path, 'r') as file:
        pInfo = json.loads(file.read())
        pw = pInfo['gmailPassword'][platform]
    return pw