# EDB3711 Lab 3 : Assignment

This source code for the blockchain part on [Building a Blockchain](https://medium.com/p/117428612f46). 

## Setup


### Docker Swarm Installation

Follow these instructions to deploy the application in swarm mode

#### 1. Clone the repository
#### 2. Build the docker container
```
$ docker build -t blockchain .
```
#### 3. Initialize new Swarm

```
$ docker swarm init --advertise-addr $(hostname -i)
```

#### 4. Deploy applications to the Swarm
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
## Documentation

### Register Nodes
You can run the `register_nodes.py` script to register all blockchain_app containers running in current swarm node. You need to run this in *all swarm nodes* to make it work consensusly across the swarm nodes.

```
$ python3 register_nodes.py
```

You will get similar looking result as follows.

```
Processes :  ['ptn7em7ei3cj', 'mzeok0kxsleb', 'aina1uglaaow']
ptn7em7ei3cj : 10.0.1.3
mzeok0kxsleb : 10.0.1.4
aina1uglaaow : 10.0.1.5

Overlay_addresses :  ['http://10.0.1.3:5000', 'http://10.0.1.4:5000', 'http://10.0.1.5:5000'] 

Containers in current swarm node :  ['ed9ef5336d66', '50f92c34bf0a', '3b30cf0b18d1']
ed9ef5336d66 : 172.18.0.9
50f92c34bf0a : 172.18.0.7
3b30cf0b18d1 : 172.18.0.8

addresses :  ['http://172.18.0.9:5000', 'http://172.18.0.7:5000', 'http://172.18.0.8:5000'] 

Registering node at  http://172.18.0.9:5000
{"nodes": ["http://10.0.1.3:5000", "http://10.0.1.4:5000", "http://10.0.1.5:5000"]}
{"message":"New nodes have been added","total_nodes":["10.0.1.4:5000","10.0.1.5:5000","10.0.1.3:5000"]}

Registering node at  http://172.18.0.7:5000
{"nodes": ["http://10.0.1.3:5000", "http://10.0.1.4:5000", "http://10.0.1.5:5000"]}
{"message":"New nodes have been added","total_nodes":["10.0.1.4:5000","10.0.1.5:5000","10.0.1.3:5000"]}

Registering node at  http://172.18.0.8:5000
{"nodes": ["http://10.0.1.3:5000", "http://10.0.1.4:5000", "http://10.0.1.5:5000"]}
{"message":"New nodes have been added","total_nodes":["10.0.1.3:5000","10.0.1.5:5000","10.0.1.4:5000"]}
```

### Automate Load
You can run the `automate.py` script to randomly call 100 blockchain operations between creating new transactions, mining new blocks, and resolving node conflicts.

```
$ python3 automate.py
```

You will get a similar looking result as follows.
```
Automating blockchain operations...

....................................................................................................
 Process finished 
```

### Resolve Nodes
You can run the `resolve_nodes.py` script to call the resolve nodes function each container in current swarm nodes. You need to run this in *all swarm nodes* if you want to make sure all chain is in consensus across all the nodes in the swarm.

```
$ python3 resolve_nodes.py
```

You will get a similar looking result as follows.
```
Containers in current swarm node :  ['03804103d71b', 'd2bddff0b4b0', '83620ab9f122']
03804103d71b : 172.18.0.6
d2bddff0b4b0 : 172.18.0.5
83620ab9f122 : 172.18.0.4

addresses :  ['http://172.18.0.6:5000', 'http://172.18.0.5:5000', 'http://172.18.0.4:5000'] 


Resolving nodes conflict...
```

### Monitoring
You can view the metrics of the containers and service on grafana. By accessing `http://localhost:3000` . the credentials are
```
user: admin
password: admin
```

For prometheus, it can be accessed at `http://localhost:9090`

### Optimization

You can access the 2 git branches for the optimized app
```
$ git checkout optimization1-modified-pow
```
or 
```
$ git checkout optimization2-scaling-pow
```


### Blockchain App API 

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

