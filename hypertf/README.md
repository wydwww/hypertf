# usage

Run these two commands, for now:

```
sh run_resource_agent.sh

python resource_matrix.py
```
Then run: 

```
python resource_manager.py
```

Open another terminal:

```
python tfcluster_runner.py 
  -p 1 
  -w 3 
  -bs 32 
  -n /home/jiacheng/benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py

```
