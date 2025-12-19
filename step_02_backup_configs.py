import json
import pickle
from typing import Dict, Optional
import netmiko
import logging
import os
from pathlib import Path
import datetime
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


class DeviceBackup:
    """
    Backup network device configurations.
    """
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    LOG_DIR = Path("/home/user/pystudies/myenv/pythonbasic/projects/backup_logs")  # Define your log directory here

    def __init__(self):
        """
        Initialize device backup step.
        """
        self.devices_inventory = {}
        self.logger = logging.getLogger()

    def load_data(self) -> None:
        """
        Load API keys from pickle file.
        """
        with open('vault_token.pkl', 'rb') as f:
            self.vault_token = pickle.load(f)

        with open('/home/user/pystudies/myenv/pythonbasic/projects/network-config-backup/data/payload/device_inventory.json', 'r') as file:
            self.devices_inventory = json.load(file)
        

    def get_config(self):
        """
        Backup configuration for a single device.
        """
        try:
            for dev in self.devices_inventory['devices']:  
                self.logger.info(f"Connecting to device {dev['hostname']} at {dev['ip_address']}")
                
                # Create device params for EACH device
                device_params = {
                    'device_type': dev['device_type'],    
                    'host': dev['ip_address'],    
                    'username': self.vault_token['username'],
                    'password': self.vault_token['password']
                }
                
                connection = ConnectHandler(**device_params)
                connection.enable()
                config = connection.send_command("show running-config")
                connection.disconnect()
                self.logger.info(f"Successfully backed up configuration for {dev['hostname']}")
                
                with open(self.LOG_DIR / f"{dev['hostname']}_{self.date_str}.txt", 'w') as config_file:
                    config_file.write(config)

        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            self.logger.error(f"Failed to connect to device: {e}")
            return None

    def execute(self) -> bool:
        """
        Execute device configuration backup.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.load_data()
            self.get_config()
            return True
        except Exception as e:
            self.logger.error(f"Error during device backup: {e}")
            return False