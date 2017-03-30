import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf
from kazoo.client import KazooClient
import allocator
import resource
import complex_MNIST as runner

# Parse input flags
tf.app.flags.DEFINE_integer("n_worker", 1, "number of worker requested")
tf.app.flags.DEFINE_integer("n_ps", 1, "number of param servers requested")
tf.app.flags.DEFINE_integer("n_gpu", 1, "number of GPUs requested")

# (optional) venv path
default_venv="source /home/jiacheng/pyenv/tf_dis/bin/activate"
# resolve possible ps and worker IP:port
use_rdma = False

# Request from service discovery
workers = alc.get_ps(FLAGS.n_worker, use_rdma)
pss = alc.get_ps(FLAGS.n_ps, use_rdma)
cluster_spec = {"ps": pss, "worker": workers}

# Connect to zookeeper node
zk = KazooClient(hosts='192.168.2.202:12181')
zk.start()
zk.ensure_path("/spec")
zk.create("/spec/node", b"ClusterSpec")

data, stat = zk.get("/spec/node")
cluster_spec = data
`
# Init training
cluster = tf.train.ClusterSpec(cluster_spec)
server = tf.train.Server(cluster, 
  job_name=resource.resolve_jobname(cluster_spec), 
  task_index=resource.resolve_taskindex(cluster_spec))

# Training with allocated device
runner.run(cluster_used, job_name, task_index, venv, protocol_used):
    

# release resource
resource.release(cluster_spec)
