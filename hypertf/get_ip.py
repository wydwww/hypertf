import netifaces as ni
from netifaces import AF_INET, AF_LINK, AF_PACKET, AF_BRIDGE
import socket
from pynvml import *

network_interface = ni.interfaces()

eth0 = ni.ifaddresses('eth0')[AF_INET][0]['addr']
eth2 = ni.ifaddresses('eth2')[AF_INET][0]['addr']
eth2_199 = ni.ifaddresses('eth2.199')[AF_INET][0]['addr']
eth3 = ni.ifaddresses('eth3')[AF_INET][0]['addr']
eth3_198 = ni.ifaddresses('eth3.198')[AF_INET][0]['addr']

def get_port(): 
    s = socket.socket() 
    s.bind(('', 0)) 
    port = s.getsockname()[1] 
    s.close()     
    return port

def get_available_gpu_index():
    gpu_list = []
    nvmlInit()
    ans = range(nvmlDeviceGetCount())
    for i in ans:
        handle = nvmlDeviceGetHandleByIndex(i)
        print "Device", i, ":", nvmlDeviceGetName(handle)
    nvmlShutdown()
    #return ans

#host = socket.gethostname() 
host = eth0
port = get_port()
addr = '%s:%s' % (host, port)
print(addr)
get_available_gpu_index()

