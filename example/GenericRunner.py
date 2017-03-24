import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf
from kazoo.client import KazooClient

# Parse input flags
tf.app.flags.DEFINE_integer("n_worker", 1, "number of worker requested")
tf.app.flags.DEFINE_integer("n_ps", 1, "number of param servers requested")
tf.app.flags.DEFINE_integer("n_gpu", 1, "number of GPUs requested")

# (optional) venv path
# generic python script path
# training python script path
# resolve possible ps and worker IP:port

FLAGS = tf.app.flags.FLAGS

# Request from service discovery
workers = resource.get_worker(FLAGS.n_worker)
pss = resource.get_ps(FLAGS.n_ps)
cluster_spec = {"ps": pss, "worker": workers}

# Connect to zookeeper node
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

zk.ensure_path("/spec")
zk.create("/spec/node", b"ClusterSpec")

data, stat = zk.get("/spec/node")

cluster_spec = data

# Init training
cluster = tf.train.ClusterSpec(cluster_spec)
server = tf.train.Server(cluster, 
  job_name=resource.resolve_jobname(cluster_spec), 
  task_index=resource.resolve_taskindex(cluster_spec))

# Training with allocated device
'''
Do training
'''

# release resource
resource.release(cluster_spec)
