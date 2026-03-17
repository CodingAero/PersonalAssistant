from datetime import datetime

def note(config, msg):
    '''
    Append a message to logs (local and Github repo)

    Input:
        config (dict): Configuration key value pairs
        msg (str): Log message
    Output:
        n/a
    '''

    try:
        with open(config['logFile'], 'a') as f:
            f.write(f"\n\n{msg}")
    except Exception as e:
        print(f"{e}:")
        print(f"An error occurred logging this message: {msg}")
    
    try:
        with open("log.txt", 'a') as f:
            f.write(f"\n\n{msg}")
    except Exception as e:
        print(f"{e}:")
        print(f"An error occurred logging this message: {msg}")
    
    return

def intializeLog(config):
    """
    Creates new, or clears existing, log files (local and Github repo)
    
    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    """

    try:
        with open(config['logFile'], 'w') as f:
            f.write("Program initialized: {0}".format(datetime.now()))
    except Exception as e:
        print(f"An error occurred initializing the Local log file: {e}")
    
    try:
        with open("log.txt", 'w') as f:
            f.write("Program initialized: {0}".format(datetime.now()))
    except Exception as e:
        print(f"An error occurred initializing the GitHub log file: {e}")
    
    note(config,f"Running {config['platform']} configuration.")
    
    return