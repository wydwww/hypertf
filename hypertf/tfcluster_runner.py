# import hypertf
import tensorflow as tf
from resource_client import client

# obtain parameters from command line.
#tf.app.flags.DEFINE_string('rm_addr', '', "ip: port of resource manager")
tf.app.flags.DEFINE_integer('ps_num', '', "number of parameter servers")
tf.app.flags.DEFINE_integer('wk_num', '', "number of workers")
tf.app.flags.DEFINE_string("app_name", "", "nature of the app, e.g. name of algorithm")

FLAGS = tf.app.flags.FLAGS
parameter_servers = FLAGS.ps_num
workers = FLAGS.wk_num
rm_addr = "http://localhost:5000" # FLAGS.rm_addr

# connect to resource manager
rm = client(rm_addr)

# request resource
pss_list, wks_list = rm.send_req(parameter_servers, workers)
resource_list = pss_list + wks_list
print "Getting resources..."
print "parameter servers: "
print pss_list
print "workers: "
print wks_list

""" compute """
print "Computing..."

# release resource
print "Release resources..."
rm.release(resource_list)




