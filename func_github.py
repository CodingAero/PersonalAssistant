import subprocess
import datetime

def update_and_push_logs(log_message):
    log_file = "run_log.txt"
    
    # 1. Update the log file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "w") as f:
        f.write(f"[{timestamp}] {log_message}\n")
    
    # 2. Execute Git commands
    try:
        # Add the specific file
        subprocess.run(["git", "add", log_file], check=True)
        
        # Commit with a message
        commit_msg = f"Auto-update logs: {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Push to the current branch
        subprocess.run(["git", "push"], check=True)
        
        print("Logs successfully pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")