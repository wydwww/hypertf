'''
' benchmark test for MNIST dataset
'''
from __future__ import print_function
import tensorflow as tf
import sys, time

workers = s.get_workers() #[]
ps = []


# define the functions that are used in the nn
#
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1,shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

#parameter_servers = ["10.40.199.203:12301", "10.40.199.202:12302", "10.40.199.201:12303","10.40.199.200:12304"]
#workers = ["10.40.199.203:12201", "10.40.199.202:12202", "10.40.199.201:12203","10.40.199.200:12204"]
parameter_servers = ["10.40.2.203:12301", "10.40.2.202:12302", "10.40.2.201:12303","10.40.2.200:12304"]
workers = ["10.40.2.203:12201", "10.40.2.202:12202", "10.40.2.201:12203","10.40.2.200:12204"]

cluster = tf.train.ClusterSpec({"ps": parameter_servers,
                                "worker": workers})


tf.app.flags.DEFINE_string("job_name", "", "Either 'ps' or 'worker'.")
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task within the job")
FLAGS = tf.app.flags.FLAGS

server = tf.train.Server(cluster,
                         job_name = FLAGS.job_name,
                         task_index = FLAGS.task_index,
                         protocol = 'grpc')

batch_size = 100
learning_rate = 0.001
training_epochs = 10
logs_path = "./conv_mnist/" + str(len(workers))

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

if FLAGS.job_name == "ps":
    server.join()
elif FLAGS.job_name == "worker":
    # Between-graph replication
    with tf.device(tf.train.replica_device_setter(
            worker_device="/job:worker/task:%d" % FLAGS.task_index, cluster=cluster)):
        global_step = tf.get_variable('global_step', [], initializer=tf.constant_initializer(0),trainable = False) 

        # input images
        with tf.name_scope('input'):
            # None -> batch size can be any size, 784 -> flattened mnist image
            x = tf.placeholder(tf.float32, shape=[None, 784], name="x-input")
            # target 10 output classes
            y_ = tf.placeholder(tf.float32, shape=[None, 10], name="y-input")
            x_image = tf.reshape(x, [-1,28,28,1])
        
        with tf.name_scope('conv1'):
            W_conv1 = weight_variable([5, 5, 1, 32])
            b_conv1 = bias_variable([32])
            h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
            h_pool1 = max_pool_2x2(h_conv1)

        with tf.name_scope('conv2'):
            W_conv2 = weight_variable([5, 5, 32, 64])
            b_conv2 = bias_variable([64])
            h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
            h_pool2 = max_pool_2x2(h_conv2)

        with tf.name_scope('dense_conn'):
            W_fc1 = weight_variable([7 * 7 * 64, 512])
            b_fc1 = bias_variable([512])
            h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
            h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32)
            h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
            
        with tf.name_scope('read_out'):
            W_fc2 = weight_variable([512, 10])
            b_fc2 = bias_variable([10])
            y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

        with tf.name_scope('cross_entropy'):
            cross_entropy = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

        with tf.name_scope('train'):
            train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        
        with tf.name_scope('prediction'):
            correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # sess.run(tf.global_variables_initializer())
        tf.summary.scalar("cost", cross_entropy)
        tf.summary.scalar("accuracy", accuracy)
        #tf.summary.scalar("time")
    
        summary_op = tf.summary.merge_all()
        print("Variables initialized")

    sv = tf.train.Supervisor(is_chief=(FLAGS.task_index==0),
                             global_step=global_step)
    start_time = time.time()
    #frequency = 100
    
    with sv.prepare_or_wait_for_session(server.target) as sess:
        writer = tf.summary.FileWriter(logs_path, graph=tf.get_default_graph())
        f = open("TCP_" + str(len(workers)) + "w_" + str(FLAGS.task_index),  'w')
        for epoch in range(training_epochs):
            batch_count=int(mnist.train.num_examples/batch_size)
            count = 0
            for i in range(batch_count):
                batch_x, batch_y = mnist.train.next_batch(batch_size)
                # run one step
                _, cost, summary, step = sess.run([train_step, cross_entropy, summary_op, global_step],
                                                  feed_dict={x:batch_x, y_:batch_y, keep_prob:0.5})
                writer.add_summary(summary,step)
                #count += 1


            elapsed_time = time.time()-start_time
            start_time = time.time()
            f.write(str(elapsed_time) + ",")
    sv.stop()
    print ("MNIST with conv. network finished")
        
