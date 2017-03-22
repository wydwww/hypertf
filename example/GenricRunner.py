import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf

# Parse input flags
tf.app.flags.DEFINE_integer("n_worker", 1, "number of worker requested")
tf.app.flags.DEFINE_integer("n_ps", 1, "number of param servers requested")
tf.app.flags.DEFINE_integer("n_gpu", 1, "number of GPUs requested")

FLAGS = tf.app.flags.FLAGS

# Request from service discovery
workers = resource.get_worker(FLAGS.n_worker)
pss = resource.get_ps(FLAGS.n_ps)
cluster_spec = {"ps": pss, "worker": workers}

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
