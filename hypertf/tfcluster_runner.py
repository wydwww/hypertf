# import hypertf
# import tensorflow as tf
from resource_client import client

# obtain parameters from command line.
#tf.app.flags.DEFINE_string('rm_addr', '', "ip: port of resource manager")
#tf.app.flags.DEFINE_string('ps_num', '', "number of parameter servers")
#tf.app.flags.DEFINE_string('wk_num', '', "number of workers")
#tf.app.flags.DEFINE_string("app_name", "", "nature of the app, e.g. name of algorithm")

#FLAGS = tf.app.flags.FLAGS
parameter_servers = 2 # FLAGS.ps_num
workers = 1 # FLAGS.wk_num
rm_addr = "http://localhost:5000" # FLAGS.rm_addr

# connect to resource manager
rm = client(rm_addr)

# request resource
resource_list = rm.send_req(parameter_servers, workers)
print resource_list

""" compute """

# release resource
rm.release(resource_list)




