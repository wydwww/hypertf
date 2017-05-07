from kazoo.client import KazooClient 
import json
from resource_manager import get_resource

zk = KazooClient(hosts='192.168.2.200:2181', read_only=True) 
zk.start()

resource = get_resource(zk)

server_range = resource.keys()
gpu_range = eval(resource.values()[0])['gpu_avail_list']

server_number, gpu_number_per_server = 4, 4 
matrix = [[1 for x in server_range] for y in gpu_range] 

print matrix
print matrix[server_range.index('node_192.168.2.203')][0]
#print(resource)

    
