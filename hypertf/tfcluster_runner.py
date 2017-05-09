# import hypertf
# import tensorflow as tf
from resource_client import client
import argparse
import subprocess
import time, sys, os

# obtain parameters from command line.
#tf.app.flags.DEFINE_string('rm_addr', '', "ip: port of resource manager")
#tf.app.flags.DEFINE_integer('ps_num', '', "number of parameter servers")
#tf.app.flags.DEFINE_integer('wk_num', '', "number of workers")
#tf.app.flags.DEFINE_string("app_name", "", "nature of the app, e.g. name of algorithm")

#FLAGS = tf.app.flags.FLAGS

# parse ps and worker arguments
parser = argparse.ArgumentParser(description='Obtain parameters.')
parser.add_argument('-p', '--ps_num', help = 'number of parameter servers', type = int, required=True)
parser.add_argument('-w', '--wk_num', help = 'number of workers', type = int, required=True)
#parser.add_argument('-g', '--GPU_num_per_server', help = 'number of GPU to use on one machine', type = int, default = 1)
args = vars(parser.parse_args())

parameter_servers = args['ps_num'] #FLAGS.ps_num
workers = args['wk_num'] #FLAGS.wk_num
rm_addr = "http://127.0.0.1:5000" # "http://localhost:5000" # FLAGS.rm_addr
#gpu_num = args['GPU_num_per_server']

# connect to resource manager
rm = client(rm_addr)

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

""" compute """
print "Computing..."
#print (str(ps_ip).replace(" ", "")+ str(wk_ip).replace(" ", ""))
time.sleep(10)

# connect to pss and workers by SSH with cluster specs

for i in res_ip_192:
    process = subprocess.Popen(["sh", "run_all.sh", str(ps_eth2).replace(" ", ""), str(wk_eth2).replace(" ", ""), str(i), str(res_ip_192.index(i)), str(gpu_index[res_ip_192.index(i)])], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

# check 'done' code from file

logdir = "/home/ywang/hypertf/hypertf/stderr/"
loglist = os.listdir(logdir)
while True:
    for logfile in loglist:
        status = open(logdir + logfile, "r")
        done = status.readlines()[-1]
        if done == "done\n":
            loglist.remove(logfile)
            print(len(loglist))
        status.close()
        time.sleep(2)
        if len(loglist) == 1:
            
            # release resource
            print("Release resources...")
            rm.release(resource_list)
            sys.exit(0)

print("Release resources...")             
rm.release(resource_list)
print resource_list
