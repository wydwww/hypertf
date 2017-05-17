# usage

1.  ```
    python resource_manager.py
    ```

Open another terminal:

2.  ```
    python tfcluster_runner.py -p 1 -w 3 \
    -- protocol grpc \
    -- batch_size 100 \
    -- learning_rate 0.001 \
    -- epoch 1 \
    -- training_script_name complex_MNIST4.py
    ```
