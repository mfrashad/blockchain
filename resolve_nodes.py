import os
import requests

stream = os.popen('sudo docker ps | grep blockchain_app | cut -d " " -f1')
containers = stream.read().splitlines()
print("Containers in current swarm node : ", containers)

addresses = []

port = 5000

for container in containers:
    stream = os.popen(f'sudo docker exec -ti {container} ifconfig eth2 | grep inet | cut -d : -f2 | cut -d " " -f1')
    ip = stream.read().strip()
    print(f'{container} : {ip}')
    addresses.append(f'http://{ip}:{port}')

print("\naddresses : ", addresses, "\n")

print('\nResolving nodes conflict...\n')

for address in addresses:
    r=requests.get(f'{address}/nodes/resolve')