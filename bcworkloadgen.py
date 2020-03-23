import requests
import json
import random
import string
import time
import numpy

headers = {"Content-Type":"application/json"}

letters=string.ascii_lowercase

address = "http://localhost:5000"



for i in range(0,100):
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