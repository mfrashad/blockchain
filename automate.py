import os
import requests
import json
import random
import string
import time
import numpy

stream = os.popen('sudo docker ps | grep blockchain_app | cut -d " " -f1')
containers = stream.read().splitlines()
print("Containers ID : ", containers, "\n")

addresses = []
port = "5000"

for container in containers:
    stream = os.popen(f'sudo docker exec -ti {container} ifconfig eth2 | grep inet | cut -d : -f2 | cut -d " " -f1')
    ip = stream.read().strip()
    print(f'{container} : {ip}')
    addresses.append(f'http://{ip}:{port}')

print("\naddresses : ", addresses, "\n")

headers = {"Content-Type":"application/json"}

for address in addresses:
    print("Registering node at ", address)
    payload = {"nodes":addresses}
    print(json.dumps(payload))
    r= requests.post(f'{address}/nodes/register', headers=headers, data=json.dumps(payload))
    print(r.text)


# print('--------------------')
print('\nAutomating blockchain operations...\n',)
# print('--------------------')

letters=string.ascii_lowercase

address = "http://localhost:5000"

for i in range(0,100):
    print(".", end='', flush=True)
    waitfor = numpy.random.exponential(0.01)
    time.sleep(waitfor)
    c = numpy.random.choice([1,2,3],p=[0.45,0.5,0.05])
    
    if c==1:
        sender = ''.join(random.choice(letters) for i in range(30))
        recipient = ''.join(random.choice(letters) for i in range(30))
        payload = {"sender":sender, "recipient":recipient, "amount":random.randint(1,20)}

        r= requests.post(address + "/transactions/new", headers=headers, data=json.dumps(payload))

    if c==2:
        r = requests.get(address + "/mine")

    if c==3:
        r=requests.get(address + "/nodes/resolve")
    
    


print('\nResolving nodes conflict...\n')

for address in addresses:
    r=requests.get(f'{address}/nodes/resolve')

print('\n Process finished \n')