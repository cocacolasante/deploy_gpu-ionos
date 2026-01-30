import requests

TEMPLATE_LIST_ENDPOINT = "https://api.ionos.com/cloudapi/v6/templates/?depth=3"
DATACENTER_UUID = "ENTER DATA CENTER UUID found in dcd"

BASE = "https://api.ionos.com/cloudapi/v6"

API_TOKEN_VALUE = "ENTER API TOKEN VALUE HERE"

GPU_S_TEMPLATE_UUID = "e15d15e7-ea9a-48ae-a60a-29b9463f4519"

GPU_TEMPLATE_ENDPOINT = f"https://api.ionos.com/cloudapi/v6/templates/{GPU_S_TEMPLATE_UUID}"

GPU_POST_ENDPOINT = f"https://api.ionos.com/cloudapi/v6/datacenters/{DATACENTER_UUID}/servers"

CREATE_LAN_ENDPOINT = f"{BASE}/datacenters/{DATACENTER_UUID}/lans"


def die_on_error(resp: requests.Response):
    if not resp.ok:
        print("STATUS:", resp.status_code)
        print("BODY:", resp.text)
        resp.raise_for_status()


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN_VALUE}",
    "Accept": "application/json"
}

LAN_PAYLOAD = {
    "properties": {
        "name": "pub-lan-1",
        "public": True
    }
}
# create the lan
resp = requests.post(CREATE_LAN_ENDPOINT, headers=headers, json=LAN_PAYLOAD, timeout=30)
die_on_error(resp)
lan_data = resp.json()
LAN_ID = lan_data["id"]
print("Created LAN:", LAN_ID)

# reserver ip block
ipblock_resp = requests.post(
    f"{BASE}/ipblocks",
    headers=headers,
    json={"properties": {"name": "gpu-static-ip", "location": "de/fra", "size": 1}},
    timeout=30,
)

die_on_error(ipblock_resp)
ipblock = ipblock_resp.json()
STATIC_IP = ipblock["properties"]["ips"][0]

print("LAN_ID:", LAN_ID)
print("STATIC_IP:", STATIC_IP)

# REQUEST TO LIST ALL TEMPLATES
# response = requests.get(
#         url=TEMPLATE_LIST_ENDPOINT,
#         headers=headers
#     )

# REQUEST FOR SPECIFIC GPU TEMPLATE S
# response = requests.get(
#         url=GPU_TEMPLATE_ENDPOINT,
#         headers=headers
#     )

server_payload = {
    "properties": {
        "name": "gputest",
        "type": "GPU",
        "availabilityZone": "AUTO",
        "templateUuid": "e15d15e7-ea9a-48ae-a60a-29b9463f4519"
    },
    "entities": {
        "volumes": {
            "items": [
                {
                    "properties": {
                        "name" : "GPU Volume",
                        "imageAlias": "ubuntu:latest",
                        "imagePassword": "ENTER CONSOLE PASSWORD HERE",
                        "sshKeys": [
                            "ENTER PUBLIC KEY HERE"
                        ]
                    }
                }
            ]
        },
        "nics": {
            "items": [
                {
                    "properties": {
                        "name" : "pub-nic-1",
                        "lan": int(LAN_ID),
                        "dhcp": True,
                        "ips": [STATIC_IP]
                    }
                }
            ]
        }
    }
}



# DELPOY THE VM
response = requests.post(
        url=GPU_POST_ENDPOINT,
        headers=headers,
        json=server_payload,
        timeout=30
    )
# error check
die_on_error(response)
server_data = response.json()
SERVER_ID = server_data["id"]


# # create the nic - ONLY USE TO CREATE A SECOND NIC
# CREATE_NIC_ENDPOINT = f"{BASE}/datacenters/{DATACENTER_UUID}/servers/{SERVER_ID}/nics"

# NIC_PAYLOAD = {
#     "properties": {
#         "name": "pub-nic-1",
#         "lan": int(LAN_ID),
#         "dhcp": True
#     }
# }

# resp = requests.post(CREATE_NIC_ENDPOINT, headers=headers, json=NIC_PAYLOAD, timeout=30)
# die_on_error(resp)
# nic_data = resp.json()
# NIC_ID = nic_data["id"]
# print("Created NIC:", NIC_ID)

print(f"Server created with {SERVER_ID} attached to Lan {LAN_ID}")