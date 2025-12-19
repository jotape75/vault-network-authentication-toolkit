import sys
import logging
import datetime
import os
from pathlib import Path


date_str = datetime.datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path("/home/user/pystudies/myenv/pythonbasic/projects/local_logging_testing")  # Define your log directory here
LOG_FILE = LOG_DIR / f"network_automation_backup_{date_str}.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',  # Append mode instead of overwrite
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

def main():

    try:
        from step_01_vault_auth import VaultClient
        VaultClient().execute()
        from step_02_backup_configs import DeviceBackup
        DeviceBackup().execute()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)    

if __name__ == "__main__":
    main()
