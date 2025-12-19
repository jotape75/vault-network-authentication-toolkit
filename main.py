"""
Network Device Configuration Backup Automation

This module serves as the main entry point for the network device backup automation system.
It orchestrates the execution of different steps including Vault authentication and device
configuration backup.

Author: [João Paulo Coutinho Pinheiro]
Created: December 2025
Version: 1.0

Dependencies:
    - HashiCorp Vault server running at http://192.168.0.206:8200
    - Network devices accessible via SSH
    - Valid Vault token with read permissions to secret/network-devices

Usage:
    python main.py

Log Output:
    - Logs are written to: /home/user/pystudies/myenv/pythonbasic/projects/Vault_authentication/logging/
    - Log filename format: network_automation_backup_YYYY-MM-DD.log
"""

import sys
import logging
import datetime
from pathlib import Path


# Global configuration
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path("/home/user/pystudies/myenv/pythonbasic/projects/Vault_authentication/logging")
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
    """
    Main execution function for network device backup automation.
    
    This function orchestrates the following steps:
    1. Authenticate with HashiCorp Vault and retrieve network device credentials
    2. Connect to network devices and backup their running configurations
    
    The function uses a modular approach where each step is implemented as a separate
    class that can be executed independently.
    
    Raises:
        SystemExit: If any critical error occurs during execution
        
    Returns:
        None
    """
    try:
        # Step 1: Authenticate with Vault and retrieve credentials
        logging.info("Starting network device backup automation")
        logging.info("Step 1: Vault authentication")
        from step_01_vault_auth import VaultClient
        VaultClient().execute()
        
        # Step 2: Backup device configurations
        logging.info("Step 2: Device configuration backup")
        from step_02_backup_configs import DeviceBackup
        DeviceBackup().execute()
        
        logging.info("Network device backup automation completed successfully")
        
    except Exception as e:
        logging.error(f"Critical error in main execution: {str(e)}")
        logging.error("Network device backup automation failed")
        sys.exit(1)


if __name__ == "__main__":
    """
    Entry point when script is run directly.
    
    This ensures the main() function is only called when the script is executed
    directly, not when imported as a module.
    """
    main()