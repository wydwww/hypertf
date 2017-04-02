'''
' structure for the Kazoo server
'
' /tf---/nodes---<list of nodes>
'     |
'     |---/masters---/master1----/ps_list
'     |            |           |
'     |---/mutex   |-/master2  |-/wk_list
'''

from kazoo.client import KazooClient
import tf_mutex as tmu
import netifaces as ni
import resource
import argparse
import thread, time

# maybe we don't need this? since
# entering the venv is required prior to starting this machine
default_venv="source /home/jiacheng/pyenv/tf_dis/bin/activate"

use_rdma = False
h_list = '192.168.2.202:12181'
device_list = [0]

# Connect to zookeeper node
# This function is executed in every node
# To report their own availability of machines
# GPUs are now idle implementation
def report(use_rdma, device_no, zk):
    zk.ensure_path("/tf/node")
    zk.ensure_path("/tf/masters")
    zk.ensure_path("/tf/mutex") # implements a mutual exclusion unit
                                # to ensure that only one read/write happens

    tmu.lock(zk)
    for i in range(len(device_list)):
        ip_port = get_ip(use_rdma)+":"+str(12200+i)
        if not zk.exists("/tf/node/"+ip_port):
            zk.create("/tf/node/"+ip_port, str(device_list[i]))
    tmu.unlock(zk)
    return

def get_ip(use_rdma):
    ip = ""
    # here substitute the corresponding name of
    # eth for rdma and tcp/ip uses correspondingly
    if use_rdma:
        ip = ni.ifaddresses('eth2.199')[2][0]['addr']
    else:
        ip = ni.ifaddresses('eth2')[2][0]['addr']
    return ip

def allocate(zk, ps_no, wk_no, use_rdma, which_master):
    all_node_list = zk.get_children('/tf/node/')
    ps_list = all_node_list[0:ps_no]
    wk_list = all_node_list[ps_no:ps_no+wk_no]
    print ps_list
    print wk_list

    if zk.exists("/tf/masters/"+ which_master + "/ps_node"):
        zk.delete("/tf/masters/" + which_master + "/ps_node/", recursive=True)
    if zk.exists("/tf/masters/"+ which_master + "/wk_node"):
        zk.delete("/tf/masters/"+ which_master + "/wk_node", recursive=True)
    zk.ensure_path("/tf/masters/"+ which_master + "/ps_node")
    zk.ensure_path("/tf/masters/"+ which_master + "/wk_node")
        

    ps_path = "/tf/masters/"+ which_master + "/ps_node/"
    wk_path = "/tf/masters/"+ which_master + "/wk_node/"

    tmu.lock(zk)
    for l in ps_list:
        if not zk.exists(ps_path + l):
            zk.create(ps_path + l)
            zk.delete("/tf/node/" + l)
    for l in wk_list:
        if not zk.exists(wk_path + l):
            zk.create(wk_path + l)
            zk.delete("/tf/node/" + l)
    tmu.unlock(zk)
    
    print ps_list
    print wk_list
    print zk.get_children('/tf/node/')
    return 

def run():
    print 111
    time.sleep(1)
    
def wait_for_call(use_rdma,zk):
    own_ip = get_ip(use_rdma)
    while True:
        master_list = zk.get_children('/tf/masters/')
        for m in master_list:
            ps_list = zk.get_children('/tf/masters/'+m+'/ps_node/')
            wk_list = zk.get_children('/tf/masters/'+m+'/wk_node/')
            
            for l in ps_list:
                if own_ip in l:
                    task_index=ps_list.index(l)
                    tmu.lock(zk)
                    ps_list.remove(l)
                    tmu.unlock(zk)
                    run()
                    tmu.lock(zk)
                    zk.delete("/tf/masters/"+m+"/ps_node/"+l, recursive=True)
                    zk.create("/tf/node/"+l)
                    tmu.unlock(zk)
        
            for l in wk_list:
                if own_ip in l:
                    task_index=wk_list.index(l)
                    tmu.lock(zk)
                    wk_list.remove(l)
                    tmu.unlock(zk)
                    run()
                    tmu.lock(zk)
                    zk.delete("/tf/masters/"+m+"/wk_node/"+l, recursive=True)
                    zk.create("/tf/node/"+l)
                    tmu.unlock(zk)

        time.sleep(5)
        print 222
        print zk.get_children('/tf/node/')
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", help="Print 1 to specify if this is master script. \n Note that there should only be one master.")
    args = parser.parse_args()
    if args.master == "1":
        print "Master node stated"
    zk = KazooClient(hosts=h_list)
    zk.start()
    parser = argparse.ArgumentParser(description='Connect to Kazoo server, or do allocation')
    report(False,1,zk)
    if args.master == "1":        
        allocate(zk,1,1,False, "1")
    wait_for_call(use_rdma,zk)
    #runner.run(cluster_used, job_name, task_index, venv, protocol_used)

    # What to do when exiting the node
