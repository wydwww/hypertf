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
args = vars(parser.parse_args())

parameter_servers = args['ps_num'] #FLAGS.ps_num
workers = args['wk_num'] #FLAGS.wk_num
rm_addr = "http://127.0.0.1:5000" # "http://localhost:5000" # FLAGS.rm_addr

# connect to resource manager
rm = client(rm_addr)

# request resource
pss_list, wks_list = rm.send_req(parameter_servers, workers)
resource_list = pss_list + wks_list
print "Getting resources..."
#print "parameter servers: "
#print pss_list
#print "workers: "
#print wks_list

ps_ip = []
wk_ip = []

ps_ip_192 = []
wk_ip_192 = []

for i in pss_list:
    ps_ip.append(str(i["ip"]))
    ps_ip_192.append("192.168" + str(i["ip"])[5:11])
for i in wks_list: 
    wk_ip.append(str(i["ip"]))
    wk_ip_192.append("192.168" + str(i["ip"])[5:11])
print "parameter servers: "
print ps_ip
print ps_ip_192
print "workers: "
print wk_ip
print wk_ip_192
res_list_192 = ps_ip_192 + wk_ip_192

""" compute """
print "Computing..."
print (str(ps_ip).replace(" ", "")+ str(wk_ip).replace(" ", ""))
index = 0

# connect to pss and workers by SSH with cluster specs
for i in res_list_192:
    #command = "sh run_all.sh " + str(i) + str(ps_ip).replace(" ", "") +str(wk_ip).replace(" ", "")
    process = subprocess.Popen(["sh", "run_all.sh", str(ps_ip).replace(" ", ""), str(wk_ip).replace(" ", ""), str(i), str(index)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    index = index + 1

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



