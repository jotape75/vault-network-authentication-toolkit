import json
import pickle
from typing import Dict, Optional
import logging
from pathlib import Path
import datetime
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


class DeviceBackup:
    """
    Network Device Configuration Backup Module

    This module handles the backup of network device configurations using SSH connections.
    It reads device inventory from a JSON file, connects to each device using credentials
    retrieved from HashiCorp Vault, and saves the running configuration to local files.

    The module supports:
    - Multiple Cisco devices (IOS/IOS-XE)
    - Parallel device connections (can be extended)
    - Error handling for connection failures
    - Configuration file management with timestamps

    Device Inventory:
        - Source: ../data/payload/device_inventory.json
        - Required fields: hostname, ip_address, device_type, vendor

    Output:
        - Configuration files saved as: {hostname}_config_backup.txt
        - Files contain complete running configuration from each device

    Dependencies:
        - netmiko library for SSH connections
        - Vault credentials from step_01_vault_auth

    Author: [João Paulo Coutinho Pinheiro]
    Created: December 2025
    Version: 1.0
    """
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    LOG_DIR = Path("/home/user/pystudies/myenv/pythonbasic/projects/Vault_authentication/devices_config_backup")  # Define your log directory here

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

        with open('/home/user/pystudies/myenv/pythonbasic/projects/Vault_authentication/data/payload/device_inventory.json', 'r') as file:
            self.devices_inventory = json.load(file)
        

    def get_config(self) -> None:
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