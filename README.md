# EDB3711 Lab 3 : Assignment

This source code for the blockchain part on [Building a Blockchain](https://medium.com/p/117428612f46). 

## Installation

1. Make sure [Python 3.6+](https://www.python.org/downloads/) is installed. 
2. Install [pipenv](https://github.com/kennethreitz/pipenv). 

```
$ pip install pipenv 
```
3. Install requirements  
```
$ pipenv install 
``` 

4. Run the server:
    * `$ pipenv run python blockchain.py` 
    * `$ pipenv run python blockchain.py -p 5001`
    * `$ pipenv run python blockchain.py --port 5002`
    
## Docker

Another option for running this blockchain program is to use Docker.  

### Docker Container

Follow the instructions below to create a local Docker container:

1. Clone this repository
2. Build the docker container

```
$ docker build -t blockchain .
```

3. Run the container

```
$ docker run --rm -p 80:5000 blockchain
```

4. To add more instances, vary the public port number before the colon:

```
$ docker run --rm -p 81:5000 blockchain
$ docker run --rm -p 82:5000 blockchain
$ docker run --rm -p 83:5000 blockchain
```

### Docker Swarm

Follow these instructions to deploy the application in swarm mode

#### 1. Clone the repository
#### 2. Initialize new Swarm

```
$ docker swarm init --advertise-addr $(hostname -i)
```

#### 3. Deploy applications to the Swarm
```
$ docker stack deploy -c docker-compose.stack.yml blockchain
```

At the end of the command, 7 services will be launched. `blockchain_app` is the blockchain application. `blockchain_caddy` as a Caddy reverse proxy server. `blockchain_cadvisor` , `blockchain_node-exporter` , `blockchain_dockerd-exporter` , `blockchain_prometheus` are the service that we use to monitor the containers and swarm nodes perfomances and metrics. Finally, `blockchain_grafana` is for the dashboard UI to display those collected metrics from prometheus into beautiful graphs.

You can confirm this by running the following command
```
$ docker service ls
```
The result will show the following services:
```
ID                  NAME                          MODE                REPLICAS            IMAGE                       PORTS
xb4xwbbf3pri        blockchain_app                replicated          3/3                 blockchain:latest           *:5000->5000/tcp
swnnneqvvi8y        blockchain_caddy              replicated          1/1                 stefanprodan/caddy:latest   *:3000->3000/tcp, *:9090->9090/tcp, *:9093-9094->9093-9094/tcp
wq7e09waxmjp        blockchain_cadvisor           global              1/1                 google/cadvisor:latest      
bc2657rzazso        blockchain_dockerd-exporter   global              1/1                 stefanprodan/caddy:latest   
p2cgjrmcjtr8        blockchain_grafana            replicated          1/1                 grafana/grafana:6.7.1       
cmt9v3j9zdxb        blockchain_node-exporter      global              1/1                 prom/node-exporter:latest   
799fg8sq15ow        blockchain_prometheus         replicated          1/1                 prom/prometheus:latest      
```

#### 4. Register nodes to blockchain app

Currently, three blockchain node will be running. However, each of the node are not aware of the neighboring nodes and not working in consensus. To make it consensus, the neighboring nodes need to be registered at each of the node.

You can confirm this by accessing `http://localhost:5000/chain`. It will randomly (based on docker swarm load balancing) direct you to any of the 3 blockchain node chain.

You will get a similar looking result
```
{"chain":[{"index":1,"previous_hash":"1","proof":100,"timestamp":1585066425.7070894,"transactions":[]}],"length":1}
```

However as you refresh, you will notice the result changes. Meaning the block chains are different at each node. And resolving the conflict by accessing `http://localhost:5000/nodes/resolve` also does not fix the issue as the node are not aware of the neighboring nodes.

The `automate.py` script will find out all the addresses of the blockchain containers/nodes (not swarm nodes) and register the nodes at each of the nodes. Additionally, it will also automate some blockchain transactions and mining operations. And finally resolve all the chain conflicts at the end.

Run the `automate.py` script.
```
$ python3 automate.py
```

The script will give a similar looking result as following
```
Containers ID :  ['dcea1c5a48d1', '91f906d06778', 'bd90ce134d93'] 

dcea1c5a48d1 : 172.18.0.9
91f906d06778 : 172.18.0.12
bd90ce134d93 : 172.18.0.11

addresses :  ['http://172.18.0.9:5000', 'http://172.18.0.12:5000', 'http://172.18.0.11:5000'] 

Registering node at  http://172.18.0.9:5000
{"nodes": ["http://172.18.0.9:5000", "http://172.18.0.12:5000", "http://172.18.0.11:5000"]}
{"message":"New nodes have been added","total_nodes":["172.18.0.12:5000","172.18.0.11:5000","172.18.0.9:5000"]}

Registering node at  http://172.18.0.12:5000
{"nodes": ["http://172.18.0.9:5000", "http://172.18.0.12:5000", "http://172.18.0.11:5000"]}
{"message":"New nodes have been added","total_nodes":["172.18.0.12:5000","172.18.0.9:5000","172.18.0.11:5000"]}

Registering node at  http://172.18.0.11:5000
{"nodes": ["http://172.18.0.9:5000", "http://172.18.0.12:5000", "http://172.18.0.11:5000"]}
{"message":"New nodes have been added","total_nodes":["172.18.0.9:5000","172.18.0.12:5000","172.18.0.11:5000"]}


Automating blockchain operations...

....................................................................................................
Resolving nodes conflict...


 Process finished 
```

Then you can confirm all the nodes are working in consensus by opening `http://localhost:5000/chain`. As you refresh, you will notice that you get the same chain every time.

Alternatively, you can access each node address directly based on result in the script. In this example it will be 
```
addresses :  ['http://172.18.0.9:5000', 'http://172.18.0.12:5000', 'http://172.18.0.11:5000'] 
```
Then you can access `http://172.18.0.9:5000/chain` to see the chain of that exact node.

#### 5. Monitoring

You can view the metrics of the containers and service on grafana. By accessing `http://localhost:3000` . the credentials are
```
user: admin
password: admin
```

For prometheus, it can be accessed at `http://localhost:9090`



## Blockchain App Usage

The following are the possible operation that you can do through the API endpoint

#### View Chain

```
http://localhost:5000/chain
```

Change the localhost to the desired blockchain node address to see the node chain

#### Add Transaction

To add transaction you need to make a POST request to `http://localhost/transactions/new` with the transaction details.

Example
```
$ curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "someone-other-address",
 "amount": 5
}' "http://localhost:5000/transactions/new"
```

#### Mine Block
```
http://localhost:5000/mine
```


#### Register New Node
To register a new node, you need to make a POST request to `http://localhost/nodes/register` with the desired addresses

Example:
```
$ curl -X POST -H "Content-Type: application/json" -d '{
 "nodes": ["http://172.18.0.9:5000", "http://172.18.0.12:5000", "http://172.18.0.11:5000"]
}' "http://localhost:5000/transactions/new"
```

#### Resolve Node Conflict

```
http://localhost:5000/nodes/resolve
```

This will choose the longest valid chain from all the registered nodes.






## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

