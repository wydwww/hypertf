from kazoo.client import KazooClient  
import json, time
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

# find a free port
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

port = []
for i in xrange(gpu):
    port.append(get_port())

def check_gpu_avail(ind, max_gpu_utilization=40, min_free_memory=50): 
    ans = True 
    nvmlInit() 
    
    # Read the gpu information multiple times
    num_times_to_average = 5
    if ind >= nvmlDeviceGetCount(): 
        ans = False 
        nvmlShutdown() 
        print (ans) 
        return ans 
    
    current_gpu_util = 0
    current_mem_util = 0
    '''    
    for i in xrange(num_times_to_average):
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(ind)
        #meminfo = nvmlDeviceGetMemoryInfo(handle)
        util = nvmlDeviceGetUtilizationRates(handle)
        #mem_util = meminfo.used/meminfo.total
        print util.gpu
        current_gpu_util += util.gpu
        current_mem_util += util.memory
        nvmlShutdown()
        time.sleep(2)

    avg_gpu_util = current_gpu_util / num_times_to_average
    avg_mem_util = current_mem_util / num_times_to_average
    print avg_gpu_util, avg_mem_util
    '''
    

    handle = nvmlDeviceGetHandleByIndex(ind)
    util = nvmlDeviceGetUtilizationRates(handle)
    meminfo = nvmlDeviceGetMemoryInfo(handle)
    print util.gpu, util.memory, meminfo    
    print meminfo.used*100/meminfo.total
    if util.gpu < max_gpu_utilization and meminfo.used*100/meminfo.total < min_free_memory:
    #if meminfo.free/meminfo.total > max_gpu_utilization:
    #if meminfo.free/1024.**2 > MBmemory_needed: 
        ans = True 
    else: 
        ans = False 
    #nvmlShutdown()
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

