# Vault Network Authentication Toolkit

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HashiCorp Vault](https://img.shields.io/badge/HashiCorp-Vault-purple.svg)](https://www.vaultproject.io/)
[![Cisco IOS](https://img.shields.io/badge/Cisco-IOS-blue.svg)](https://www.cisco.com/)
[![Network Automation](https://img.shields.io/badge/Network-Automation-green.svg)](https://github.com/jotape75/vault-network-authentication-toolkit)

A Python toolkit for securely authenticating with HashiCorp Vault and using retrieved credentials to backup network device configurations. This tool demonstrates enterprise-grade credential management for network automation workflows.

Perfect for network engineers learning HashiCorp Vault integration with network device automation.

## Overview

This toolkit provides a **secure authentication workflow** using HashiCorp Vault to retrieve network device credentials and perform configuration backups. It eliminates hardcoded credentials and demonstrates best practices for credential management in network automation.

## Primary Use Cases

- **Secure Credential Retrieval**: HashiCorp Vault integration for network device credentials  
- **Network Device Access**: SSH-based connection to Cisco network devices  
- **Configuration Backup**: Automated running configuration backup to local files  
- **Vault Authentication Testing**: Validate Vault connectivity and credential storage  

## Key Features

- **HashiCorp Vault Integration**: Secure credential storage and retrieval  
- **Network Device SSH**: Netmiko-based device connections  
- **Configuration Backup**: Save running configs to local files  
- **Error Handling**: Robust connection and authentication error handling  
- **Comprehensive Logging**: Detailed logging for troubleshooting  
- **Modular Design**: Clean, reusable code structure  

## Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Python Script     │────▶│  HashiCorp Vault │────▶│  Network Devices    │
│  - Vault Client    │     │  - Credentials   │     │  - Cisco Switches   │
│  - Device Backup   │     │  - Audit Logs    │     │  - Running Config   │
└─────────────────────┘     └──────────────────┘     └─────────────────────┘
           │                                                     │
           ▼                                                     ▼
┌─────────────────────┐                               ┌─────────────────────┐
│  Local Files        │                               │  Application Logs   │
│  - Config Backups  │                               │  - Vault Auth       │
│  - Device Inventory │                               │  - Device Access    │
└─────────────────────┘                               └─────────────────────┘
```

## Project Structure

```
vault-network-toolkit/
├── src/
│   ├── vault_client.py                 # Vault authentication and credential retrieval
│   └── steps/
│       ├── step_01_vault_auth.py      # Vault connectivity testing
│       └── step_02_backup_configs.py   # Device backup functionality
├── data/
│   └── payload/
│       └── device_inventory.json       # Network device inventory
├── log/                               # Application logs
├── configs/                           # Local configuration backups
├── requirements.txt                   # Python dependencies
├── LICENSE                           # MIT License
└── README.md                          # This documentation
```

## Installation & Setup

### Prerequisites

1. **HashiCorp Vault Server** running and accessible
2. **Python 3.8+** with pip
3. **Network connectivity** to target devices
4. **SSH access** to network devices

### HashiCorp Vault Setup

```bash
# Install and configure Vault server
sudo apt install vault
sudo systemctl start vault

# Initialize and unseal Vault
vault operator init
vault operator unseal <key1> <key2> <key3>

# Login and enable KV secrets engine
vault login <root_token>
vault secrets enable -path=secret kv-v2

# Store network device credentials
vault kv put secret/network-devices \
    username=automation_user \
    password=YourNetworkPassword123!
```

### Python Environment Setup

```bash
# Clone or download the toolkit
git clone https://github.com/jotape75/vault-network-authentication-toolkit.git
cd vault-network-authentication-toolkit

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Device Inventory Configuration

Update `data/payload/device_inventory.json` with your network devices:

```json
{
  "devices": [
    {
      "hostname": "ciscowansw01",
      "ip_address": "192.168.0.238",
      "device_type": "cisco_ios",
      "type": "switch",
      "vendor": "cisco"
    },
    {
      "hostname": "ciscowansw02", 
      "ip_address": "192.168.0.239",
      "device_type": "cisco_ios",
      "type": "switch",
      "vendor": "cisco"
    }
  ]
}
```

## Usage

### Environment Variables

```bash
# Set Vault configuration
export VAULT_ADDR='http://192.168.0.206:8200'
export VAULT_TOKEN='your_vault_token_here'
```

### Running the Toolkit

```bash
# Test Vault connectivity and credential retrieval
python src/vault_client.py

# Test individual components
python src/steps/step_01_vault_auth.py      # Vault authentication test
python src/steps/step_02_backup_configs.py  # Device backup test

# Run complete backup process
python src/main.py
```

### Expected Output

```bash
# Vault authentication success
2025-12-19 11:29:23 - INFO - Successfully connected to Vault
2025-12-19 11:29:23 - INFO - Retrieved credentials successfully

# Device backup success  
2025-12-19 11:29:24 - INFO - Connecting to device ciscowansw01 at 192.168.0.238
2025-12-19 11:29:27 - INFO - Successfully backed up configuration for ciscowansw01

# Local files created
configs/ciscowansw01_config_backup.txt
configs/ciscowansw02_config_backup.txt
```

## Core Components

### Vault Client (`vault_client.py`)

| Function | Purpose | Returns |
|----------|---------|---------|
| `connect()` | Authenticate with Vault server | Boolean success status |
| `get_network_credentials()` | Retrieve device credentials | Dict with username/password |
| `execute()` | Full connectivity test | Logged results |

### Device Backup (`step_02_backup_configs.py`)

| Function | Purpose | Output |
|----------|---------|--------|
| `load_devices()` | Read device inventory JSON | Device list |
| `get_config()` | SSH to devices and backup configs | Local config files |
| `execute()` | Run complete backup process | Logged results |

### Supported Devices

| Vendor | Device Type | Netmiko Driver | Status |
|--------|-------------|----------------|--------|
| **Cisco** | IOS/IOS-XE Switches | `cisco_ios` | ✅ Tested |
| **Cisco** | IOS/IOS-XE Routers | `cisco_ios` | ✅ Compatible |

## Logging and Monitoring

### Log Files

```bash
# Default log location
/home/user/pystudies/myenv/pythonbasic/projects/Vault_authentication/logging/
network_automation_backup_YYYY-MM-DD.log

# Log levels
- INFO: Successful operations
- ERROR: Connection failures, authentication issues
```

### Sample Log Output

```
2025-12-19 11:29:23 - INFO - Successfully connected to Vault
2025-12-19 11:29:23 - INFO - Retrieved credentials successfully
2025-12-19 11:29:24 - INFO - Connecting to device ciscowansw01 at 192.168.0.238
2025-12-19 11:29:27 - INFO - Successfully backed up configuration for ciscowansw01
2025-12-19 11:29:28 - INFO - Configuration saved to: ciscowansw01_config_backup.txt
```

## Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Vault Connection Failed** | Wrong URL or token | Verify `VAULT_ADDR` and `VAULT_TOKEN` |
| **Permission Denied** | Invalid Vault token | Check token permissions with `vault token lookup` |
| **Device SSH Failure** | Network/credential issues | Verify device IP and SSH access |
| **Import Error** | Missing dependencies | Run `pip install -r requirements.txt` |

### Testing Commands

```bash
# Test Vault connectivity
vault status

# Verify stored credentials  
vault kv get secret/network-devices

# Test device SSH manually
ssh automation_user@192.168.0.238

# Verify Python dependencies
pip list | grep -E "(netmiko|hvac)"
```

## Security Best Practices

### Production Recommendations

```bash
# Use environment variables for sensitive data
export VAULT_TOKEN=$(vault write -field=token auth/aws/login role=network-automation)

# Rotate credentials regularly
vault kv put secret/network-devices username=new_user password=new_password

# Enable Vault audit logging
vault audit enable file file_path=/var/log/vault/audit.log
```

### Security Checklist

- **No Hardcoded Credentials**: All credentials stored in Vault
- **Environment Variables**: Use environment variables for tokens
- **Token Expiration**: Use short-lived Vault tokens
- **Audit Logging**: Enable comprehensive audit trails
- **Secure Storage**: Never commit tokens to version control

## Roadmap

### Future Enhancements

- **Multi-Vendor Support**: Palo Alto, Arista, Fortinet
- **Git Integration**: Version control for configurations
- **HTML Reporting**: Backup success/failure reports
- **Multithreading**: Parallel device connections
- **Jenkins Pipeline**: CI/CD integration

## Contributing

This toolkit serves as a foundation for learning Vault integration with network automation. Contributions for additional features or vendor support are welcome!

## Contact

**João Paulo Coutinho Pinheiro**

[![GitHub](https://img.shields.io/badge/GitHub-jotape75-blue?style=flat&logo=github)](https://github.com/jotape75)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaopaulocp-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/joaopaulocp/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **HashiCorp Vault** for secure secrets management
- **Netmiko library** for network device automation  
- **Cisco DevNet** for network automation resources

---

**Star this repository** if it helps with your Vault and network automation learning journey!

**Perfect starting point** for learning enterprise credential management in network automation.