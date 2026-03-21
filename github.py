import subprocess
import datetime
import logger as log

def githubLog(config):
    '''
    Send log.txt to Github repository.

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: githubLog")
    
    log_file = "log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Add the specific file
        add_result = subprocess.run(["git", "add", log_file], check=True, capture_output=True, text=True)
        
        # Commit with a message
        commit_msg = f"Personal Assistant Logs: {timestamp}"
        commit_result = subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True, text=True)
        
        # Push to the current branch
        push_result = subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
        
        # Store the outputs
        git_output = f"Add Output:\n{add_result.stdout}\nCommit Output:\n{commit_result.stdout}\nPush Output:\n{push_result.stdout}"
        
        # Log the Git command outputs
        log.note(config,f"githubLog: GITHUB RESPONSE:\n{git_output}")
        log.note(config,"githubLog: Logs successfully pushed to GitHub.")
        
    except subprocess.CalledProcessError as e:
        log.note(config,f"githubLog: ERROR DURING GITHUB OPERATIONS\n    Error: {e}")