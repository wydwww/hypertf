#!/bin/bash

ssh 192.168.2.200 "source /home/jiacheng/pyenv/tf_dis/bin/activate && cd /home/ywang/hypertf/hypertf && python resource_agent.py &"

ssh 192.168.2.201 "source /home/jiacheng/pyenv/tf_dis/bin/activate && cd /home/ywang/hypertf/hypertf && python resource_agent.py &"

ssh 192.168.2.202 "source /home/jiacheng/pyenv/tf_dis/bin/activate && cd /home/ywang/hypertf/hypertf && python resource_agent.py &"

ssh 192.168.2.203 "source /home/jiacheng/pyenv/tf_dis/bin/activate && cd /home/ywang/hypertf/hypertf && python resource_agent.py &"

python resource_matrix.py
