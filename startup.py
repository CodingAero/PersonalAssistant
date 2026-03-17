import json
import os

def configPath(verbose=False):
    '''
    Provide the configuration file path to keep real data out of the github
    repository and prevent computer specific reconfigurations.

    Input:
        verbose (bool): Print additional terminal messages
    Output:
        config_path (str): File path to the configuration file
    '''

    # Hardcoded config paths in preferred order
    configs = {
        'windows':  'C:/Users/smith/LocalConfig/PersonalAssistant/personal_assistant.json',
        'mac':      '/Users/smith/local_config/personal_assistant.json',
        'ubuntu':   '/home/smith/Documents/Code/local_config/personal_assistant/personal_assistant.json',
        'default':  'config.json'
    }

    # Initialize the config path variable
    config_path = ''

    # Check for the existence of the configuration file in the hardcoded paths
    for c in configs.keys():
        if os.path.exists(configs[c]):
            config_path = configs[c]
            if verbose: print("Using '{0}' configuration.".format(str(c)))
            break
    
    # If the configuration file was not found in any of the hardcoded paths, exit program
    if config_path == '':
        print("Unable to locate a file containing your configuration.")
        exit()

    return config_path

def get_config():
    '''
    Retrieve configuration variables.

    Input:
        n/a
    Output:
        config (dict): Configuration key value pairs
    '''
    path = configPath(True)

    # Note: Find the configuration items in config.json
    with open(path) as file:
        config = json.loads(file.read())
    
    # Append config path
    config['configPath'] = path

    return config