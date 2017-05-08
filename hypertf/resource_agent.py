from kazoo.client import KazooClient  
import json
import netifaces as ni
from netifaces import AF_INET, AF_LINK, AF_PACKET, AF_BRIDGE 
import socket 
from pynvml import *
import argparse

zk = KazooClient(hosts='192.168.2.200:2181', read_only=True) 
zk.start()

network_interface = ni.interfaces()

eth0 = ni.ifaddresses('eth0')[AF_INET][0]['addr']
eth2 = ni.ifaddresses('eth2')[AF_INET][0]['addr']

def get_port(): 
    s = socket.socket() 
    s.bind(('', 0)) 
    port = s.getsockname()[1] 
    s.close() 
    return port

port = get_port()

addr = '%s:%s' % (eth2, port)

def get_available_gpu_index(): 
    gpu_list = [] 
    nvmlInit() 
    gpu_count = nvmlDeviceGetCount()
    nvmlShutdown()
    return int(gpu_count)

gpu = get_available_gpu_index()

def check_gpu_avail(ind, MBmemory_needed=20000): 
    ans = True 
    nvmlInit() 
    if ind >= nvmlDeviceGetCount(): 
        ans = False 
        nvmlShutdown() 
        print (ans) 
        return ans 
    handle = nvmlDeviceGetHandleByIndex(ind) 
    meminfo = nvmlDeviceGetMemoryInfo(handle) 
    if meminfo.free/1024.**2 > MBmemory_needed: 
        ans = True 
    else: 
        ans = False 
    nvmlShutdown()
    output = "No. %s GPU available? " % str(ind)
    print(output + str(ans)) 
    return ans

gpu_avail_list = []

for i in xrange(gpu):
    if check_gpu_avail(i):
        gpu_avail_list.append(i)
    
resource_node = {
    #"idle": 1,
    #"id": args['id'],
    "eth0": eth0,
    "eth2": eth2,
    "port": port,
    "gpu": gpu,
    "gpu_avail_list": gpu_avail_list
}

print(resource_node)

node_name = "resources/node_%s" % eth0

zk.ensure_path("resources")
if zk.exists(node_name):
    zk.set(node_name, json.dumps(resource_node))
else:
    zk.create(node_name, json.dumps(resource_node))

