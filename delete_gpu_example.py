import os
import requests

BASE = "https://api.ionos.com/cloudapi/v6"
DATACENTER_ID = "93d4758f-3fe5-4526-88de-05e558fc03bf"
SERVER_ID = "04e2eb23-524e-42ae-9248-6d4c61d9b001"  # <-- GPU server ID

API_TOKEN_VALUE = "ENTER TOKEN VALUE HERE"

headers = {
    "Authorization": f"Bearer {API_TOKEN_VALUE}",
    "Accept": "application/json",
}

delete_url = f"{BASE}/datacenters/{DATACENTER_ID}/servers/{SERVER_ID}"

resp = requests.delete(delete_url, headers=headers, timeout=30)

print("Status:", resp.status_code)

if resp.status_code not in (202, 204):
    print("Body:", resp.text)
    resp.raise_for_status()

print("Delete request accepted.")