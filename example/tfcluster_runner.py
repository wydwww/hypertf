import hypertf
import tensorflow as tf

# obtain parameters from command line.
tf.app.flags.DEFINE_string('rm_addr', '', "ip: port of resource manager")
tf.app.flags.DEFINE_string('ps_num', '', "number of parameter servers")
tf.app.flags.DEFINE_string('wk_num', '', "number of workers")
tf.app.flags.DEFINE_string("app_name", "", "nature of the app, e.g. name of algorithm")

FLAGS = tf.app.flags.FLAGS
parameter_servers = FLAGS.ps_num
workers = FLAGS.wk_num
rm_addr = FLAGS.rm_addr

# connect to resource manager
rm = hypertf.resource_manager(rm_addr)

# request resource
rm.send_req([parameter_servers, workers])
resource_list = rm.recv_res()

""" compute """

# release resource
rm.release()




