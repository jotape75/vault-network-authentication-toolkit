import hvac
import logging
from typing import Dict, Optional
import pickle

class VaultClient: 
    """
    HashiCorp Vault Authentication Module

    This module provides functionality to authenticate with HashiCorp Vault and retrieve
    network device credentials securely. It uses the hvac library to interact with the
    Vault API and implements proper error handling and logging.

    The module is designed to:
    - Connect to a Vault server using a token-based authentication
    - Retrieve network device credentials from a KV v2 secrets engine
    - Provide logging for audit and troubleshooting purposes

    Configuration:
        - Vault Server: http://192.168.0.206:8200
        - Secrets Path: secret/network-devices
        - Expected Credentials: username, password

    Author: [João Paulo Coutinho Pinheiro]
    Created: December 2025
    Version: 1.0
    """

    def __init__(self):
        """
        Initialize Vault client
        """
        self.client = None
        self.creds = None
        self.logger = logging.getLogger()


    def connect(self) -> bool:
        """
        Authenticate to Vault and create a client
        """

        # Vault configuration
        self.VAULT_URL = 'http://192.168.0.206:8200'
        self.VAULT_TOKEN = 'YOUR_ROOT_TOKEN' #for testing only. Use secure methods in production
        """
        Connect to Vault server
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = hvac.Client(url=self.VAULT_URL)
            self.client.token = self.VAULT_TOKEN
            
            # Test connection
            if not self.client.is_authenticated():
                self.logger.error("Vault authentication failed")
                return False
                
            self.logger.info("Successfully connected to Vault")
            return True
            
        except Exception as e:
            return False
        
    def get_network_credentials(self) -> Optional[Dict[str, str]]:
        """
        Retrieve network device credentials from Vault
        
        Returns:
            dict: Dictionary containing username and password, or None if failed
        """
        try:
            if not self.client:
                self.logger.error("Vault client not initialized")
                return None
                
            secret_response = self.client.secrets.kv.v2.read_secret_version(
                path='network-devices'
            )
            
            # Get json secret_response for debugging /checking schema
            self.logger.info(secret_response) # Log the entire secret response for debugging, remove in production

            credentials = {
                'username': secret_response['data']['data']['username'],
                'password': secret_response['data']['data']['password']
            }
            
            return credentials
            
        except Exception as e:
            return None

    def execute(self) -> None:
        """
        Main execution method to connect to Vault and retrieve credentials
        """
        if self.connect():
            self.creds = self.get_network_credentials()
            if self.creds:
                self.logger.info(f"Retrieved credentials: {self.creds}")
                with open('vault_token.pkl', 'wb') as f:
                    pickle.dump(self.creds, f)
            else:
                self.logger.error("Could not retrieve credentials")
        else:
            self.logger.error("Could not connect to Vault")