import requests
import json
import random
import string
import time
import numpy

headers = {"Content-Type":"application/json"}

address = "http://localhost:5001"

payload = {"last_proof":100, "last_hash":"1",}

r= requests.post(address + "/pow", headers=headers, data=json.dumps(payload))
print(json.loads(r.text)['proof'])