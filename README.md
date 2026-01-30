# Deploy GPU VM on IONOS Cloud

Automated Python scripts for deploying and managing GPU virtual machines on IONOS Cloud infrastructure using the IONOS Cloud API.

## Overview

This project provides Python scripts to:
- **Deploy GPU VMs** with automated LAN and static IP configuration
- **Delete GPU VMs** and associated resources
- Provision Ubuntu-based GPU servers with SSH access
- Automatically configure networking (LAN, NIC, static IP blocks)

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)
- IONOS Cloud account with API access
- Data Center UUID from IONOS DCD (Data Center Designer)
- API token with appropriate permissions

## Project Structure

```
deploy_gpu/
├── deploy_gpu.py           # Main deployment script with hardcoded values
├── deploy_gpu_example.py   # Template script with placeholder values
├── delete_gpu_example.py   # Script to delete GPU server instances
└── README.md              # This file
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/cocacolasante/deploy_gpu-ionos
cd deploy_gpu
```

### 2. Configure Your Credentials

You can either modify `deploy_gpu_example.py` or create your own copy. Update the following values:

#### Required Configuration (deploy_gpu_example.py)

- **Line 4**: `DATACENTER_UUID` - Your Data Center UUID from IONOS DCD
- **Line 8**: `API_TOKEN_VALUE` - Your IONOS Cloud API token
- **Line 86**: `imagePassword` - Console password for the VM
- **Line 88**: `sshKeys` - Your public SSH key
- **Line 88**: change deploy_gpu_example.py to deploy_gpu.py

#### Get Data Center UUID
1. Log into IONOS DCD (Data Center Designer)
2. Navigate to your data center
3. Copy the Data Center UUID from the URL or data center details

#### Get API Token
1. Log into IONOS DCD
2. Navigate to API settings
3. Generate a new API token
4. Copy the token value immediately (it won't be shown again)

### 3. Install Dependencies

```bash
pip install requests
```

## Usage

### Deploy a GPU VM

```bash
python deploy_gpu_example.py
```

This script will:
1. Create a public LAN
2. Reserve a static IP block in Frankfurt (de/fra)
3. Deploy a GPU server with:
   - GPU type: GPU S (template UUID: `e15d15e7-ea9a-48ae-a60a-29b9463f4519`)
   - OS: Ubuntu (latest)
   - Configured NIC with static IP
   - SSH access enabled

### Delete a GPU VM

Update `delete_gpu.py` with:
- **Line 5**: `DATACENTER_ID` - Your Data Center UUID
- **Line 6**: `SERVER_ID` - The server ID to delete (returned after deployment)
- **Line 8**: `API_TOKEN_VALUE` - Your IONOS Cloud API token

```bash
python delete_gpu.py
```

## Configuration Details

### GPU Template
- The scripts use GPU S template (UUID: `e15d15e7-ea9a-48ae-a60a-29b9463f4519`)
- Location: Frankfurt (de/fra)
- Availability Zone: AUTO

### Networking
- Creates a public LAN named "pub-lan-1"
- Reserves a static IP block (size: 1)
- Configures NIC with DHCP and static IP assignment

## Security Notes

**IMPORTANT**:
- Never commit files with real API tokens or passwords to version control
- The `deploy_gpu.py` file contains actual credentials and should be added to `.gitignore`
- Use `deploy_gpu_example.py` as a template with placeholder values
- Rotate your API tokens regularly
- Use strong passwords for VM console access

## Troubleshooting

### Common Issues

**API Authentication Error**
- Verify your API token is valid and hasn't expired
- Ensure the token has necessary permissions (DATA_CENTER_CREATE, IP_BLOCK_RESERVE, etc.)

**Data Center Not Found**
- Double-check your DATACENTER_UUID
- Ensure the data center exists in your IONOS account

**Deployment Timeout**
- IONOS provisioning can take several minutes
- Check the IONOS DCD console for deployment status

**IP Block Reservation Fails**
- Verify your account has IP block reservation privileges
- Check if you've reached your IP block quota

## API Reference

This project uses the IONOS Cloud API v6:
- Base URL: `https://api.ionos.com/cloudapi/v6`
- GPU Documentation: `https://docs.ionos.com/cloud/compute-services/compute-engine/cloud-gpu-vm/api-how-tos`

## License

