# hypertf
Tensorflow Hyperparameter Tuning Framework

## dependency

ZooKeeper and kazoo, flask and flask_restful, netifaces, pynvml

## code format

1. According to examples in benchmarks, list of target hosts should be comma-separated, then use 
```
self.ps_hosts = FLAGS.ps_hosts.split(',')
```
​	in the code to split the list.

2. Add this 1 line to the end of the main function:
```
sys.exit("done")
```

## usage

- start ZooKeeper service and update server address in the code

- run ```resource agent```:

```
sh ./hypertf/run_resource_agent.sh

```

- then start resource manager service:

```
python ./hypertf/resource_manager.py &
```

- run a distributed TensorFlow training program with TFCluster Runner:

```
python ./hypertf/tfcluster_runner.py   
    -p 1 
    -w 3 
    -bs 32 
    -n .../tf_cnn_benchmarks/tf_cnn_benchmarks.py
    ...
```

​	HyperTF can take:

1. ```-p``` or ```--ps_num```, number of parameter server

2. ```-w``` or ```--wk_num```, number of worker

3. ```-ptc``` or ```--protocol```, protocol to use, grpc or rdma

4. ```-bs``` or ```--batch_size```, batch size

5. ```-lr``` or ```--learning_rate```, learning rate

6. ```-n``` or ```--training_script_name```, script path

