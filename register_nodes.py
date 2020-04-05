import os
import requests
import json

stream = os.popen('sudo docker node ps $(sudo docker node ls -q) --filter desired-state=Running | uniq | grep blockchain_app | cut -d " " -f1')
processes = stream.read().splitlines()
print("Processes : ", processes)
overlay_addresses = []

port = "5000"

for process in processes:
    stream = os.popen(f'sudo docker inspect {process} | grep "10.0." | grep ":" -v | cut -d / -f1 | sed \'s/[ "]//g\'')
    ip = stream.read().strip()
    print(f'{process} : {ip}')
    overlay_addresses.append(f'http://{ip}:{port}')

print("\nOverlay_addresses : ", overlay_addresses, "\n")

stream = os.popen('sudo docker ps | grep blockchain_app | cut -d " " -f1')
containers = stream.read().splitlines()
print("Containers in current swarm node : ", containers)

addresses = []

for container in containers:
    stream = os.popen(f'sudo docker exec -ti {container} ifconfig eth2 | grep inet | cut -d : -f2 | cut -d " " -f1')
    ip = stream.read().strip()
    print(f'{container} : {ip}')
    addresses.append(f'http://{ip}:{port}')

print("\naddresses : ", addresses, "\n")

headers = {"Content-Type":"application/json"}

for address in addresses:
    print("Registering node at ", address)
    payload = {"nodes":overlay_addresses}
    print(json.dumps(payload))
    r= requests.post(f'{address}/nodes/register', headers=headers, data=json.dumps(payload))
    print(r.text)


