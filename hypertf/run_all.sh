#!/bin/bash

ssh $3 "source /home/jiacheng/pyenv/tf_dis/bin/activate && cd /home/ywang/hypertf/hypertf && sh run1.sh $4 $1 $2"
sleep 10
# worker 1
# ssh $3 "source ~/pyenv/tf_dis/bin/activate && cd scripts/tensorflow_standard/new_test && sh run.sh 1 $1 $2"
# worker 2
# ssh $3 "source ~/pyenv/tf_dis/bin/activate && cd scripts/tensorflow_standard/new_test && sh run.sh 2 $1 $2"
# worker 3
# ssh $3 "source ~/pyenv/tf_dis/bin/activate && cd scripts/tensorflow_standard/new_test && sh run.sh 3 $1 $2"

