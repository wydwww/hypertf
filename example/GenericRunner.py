#import tensorflow as tf
from kazoo.client import KazooClient
import netifaces as ni
import resource
#import complex_MNIST as runner
import argparse

# Parse input flags

# (optional) venv path
default_venv="source /home/jiacheng/pyenv/tf_dis/bin/activate"
use_rdma = False
h_list = '192.168.2.202:12181'
device_list = [0,1]

# Connect to zookeeper node
def report(use_rdma, device_no):
    zk = KazooClient(hosts=h_list)
    zk.start()
    zk.ensure_path("/tf/node")
    zk.ensure_path("/tf/ps_node")
    zk.ensure_path("/tf/wk_node")
    
    for i in range(len(device_list)):
        ip_port = get_ip(use_rdma)+":"+str(12200+i)
        if not zk.exists("/tf/node/"+ip_port):
            zk.create("/tf/node/"+ip_port, str(device_list[i]))
    return

def get_ip(use_rdma):
    ip = ""
    if use_rdma:
        ip = ni.ifaddresses('eth2')[2][0]['addr']
    else:
        ip = ni.ifaddresses('eth2.199')[2][0]['addr']
    return ip

def allocate(zk, ps_no, wk_no, use_rdma):
    all_node_list = zk.get_children('/tf/node/')
    ps_list = all_node_list[0:ps_no]
    wk_list = all_node_list[ps_no:ps_no+wk_no]
    print ps_list
    print wk_list
    
    zk.delete("/tf/ps_node")
    zk.delete("/tf/wk_node")
    zk.ensure_path("/tf/ps_node")
    zk.ensure_path("/tf/wk_node")
    
    for l in ps_list:
        zk.create("/tf/ps_node" + l)
    for l in wk_list:
        zk.create("/tf/wk_node" + l)

        
if __name__ == '__main__':
    zk = KazooClient(hosts=h_list)
    zk.start()
    parser = argparse.ArgumentParser(description='Connect to Kazoo server, or do allocation')
    report(False,2)
    # if it is master we change
    allocate(zk,1,1,False)

    #runner.run(cluster_used, job_name, task_index, venv, protocol_used)
