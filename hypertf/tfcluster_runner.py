# import hypertf
# import tensorflow as tf
from resource_client import client
import argparse
import subprocess
import time, sys, os
import logging

logger = logging.getLogger(__name__)

# parse parameters from command line
parser = argparse.ArgumentParser(description='Obtain parameters.')
parser.add_argument('-p', '--ps_num', help = 'number of parameter servers', type = int, required=True)
parser.add_argument('-w', '--wk_num', help = 'number of workers', type = int, required=True)
parser.add_argument('-ptc', '--protocol', help = 'protocol to use, grpc or rdma', default='grpc', type=str)
#parser.add_argument('-g', '--GPU_num_per_server', help = 'number of GPU to use on one machine', type = int, default = 1)
parser.add_argument('-bs', '--batch_size', type = int, default = 110)
parser.add_argument('-lr', '--learning_rate', type = float, default = 0.001)
parser.add_argument('-e', '--epoch', type = int, default = 1)
parser.add_argument('-n', '--training_script_name', type = str, default = 'complex_MNIST4.py')

args = vars(parser.parse_args())

parameter_servers = args['ps_num'] #FLAGS.ps_num
workers = args['wk_num'] #FLAGS.wk_num
rm_addr = "http://127.0.0.1:5000" # "http://localhost:5000" # FLAGS.rm_addr
#gpu_num = args['GPU_num_per_server']
protocol = args['protocol']
script_name = args['training_script_name']

# hyperparameters
batch_size = args['batch_size']
learning_rate = args['learning_rate']
epoch = args['epoch']

logger.info('Get hyperparameters from command line.\n number of parameter servers: {} \n number of workers: {}'.format(parameter_servers, workers))

# connect to resource manager
rm = client(rm_addr)
logger.info('Connected to resource manager: {}'.format(rm_addr))

# request resource
pss_list, wks_list = rm.send_req(parameter_servers, workers)
resource_list = pss_list + wks_list
print "Getting resources..."
print "parameter servers: "
for i in pss_list:
    print i
print "workers: "
for i in wks_list:
    print i

ps_eth2 = []
wk_eth2 = []
ps_eth0 = []
wk_eth0 = []
gpu_index = []

for i in pss_list:
    ps_eth2.append(eval(i[0])['eth2']+':'+str(eval(i[0])['port']))
    ps_eth0.append(eval(i[0])['eth0'])

for i in wks_list: 
    wk_eth2.append(eval(i[0])['eth2']+':'+str(eval(i[0])['port']))
    wk_eth0.append(eval(i[0])['eth0'])

for i in resource_list:
    gpu_index.append(i[1])

res_ip_192 = ps_eth0 + wk_eth0

print "parameter servers: "
print ps_eth0
print "workers: "
print wk_eth0
print "gpu index:"
print gpu_index

logger.info('Get resource.\n ps: {} \n worker: {} \n gpu: {}'.format(ps_eth0, wk_eth0, gpu_index))

""" compute """
print "Computing..."
#print (str(ps_ip).replace(" ", "")+ str(wk_ip).replace(" ", ""))
time.sleep(10)

# connect to pss and workers by SSH with cluster specs

for i in ps_eth0:
    print "ps:"
    print i
    process = subprocess.Popen(["sh", "run_all.sh", str(ps_eth2).replace(" ", ""), str(wk_eth2).replace(" ", ""), str(i), str(ps_eth0.index(i)), str(gpu_index[res_ip_192.index(i)]), str(batch_size), str(learning_rate), str(epoch), protocol, 'ps', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)

for i in wk_eth0:
    print 'wk:'
    print i 
    process = subprocess.Popen(["sh", "run_all.sh", str(ps_eth2).replace(" ", ""), str(wk_eth2).replace(" ", ""), str(i), str(wk_eth0.index(i)), str(gpu_index[res_ip_192.index(i)]), str(batch_size), str(learning_rate), str(epoch), protocol, 'worker', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)

# check 'done' code from file
time.sleep(15)
logdir = "/home/ywang/hypertf/hypertf/stderr/"
filelist = os.listdir(logdir)
success_counter = 0
loglist = []

while len(loglist) != len(gpu_index):
    for i in filelist:
        if os.path.splitext(i)[1] == '.log' and i not in loglist:
            loglist.append(i)

while True:
    for logfile in loglist:
        status = open(logdir + logfile, "r")
        done = status.readlines()[-1]
        if done == "done\n":
            success_counter += 1
            loglist.remove(logfile)
            print(success_counter)
        status.close()
        time.sleep(2)
        if success_counter == len(wk_eth0):
            
            # release resource
            print("Release resources...")
            rm.release(resource_list)
            logger.info('Release resource. Exit.')
            sys.exit(0)

