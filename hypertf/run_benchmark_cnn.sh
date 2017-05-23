#!/bin/bash

LOC="/home/ywang/hypertf/hypertf"
SOURCE_CMD="source /home/jiacheng/pyenv/tf_roc2/bin/activate"
dir=./stdout/ 
direrr=./stderr/

ssh $3 "$SOURCE_CMD && cd $LOC && CUDA_VISIBLE_DEVICES=$5 python $11 --local_parameter_device=cpu --num_gpus=1 --model=resnet50 --variable_update=parameter_server --job_name=$10 --ps_hosts=$1 --worker_hosts=$2 --task_index=$4 --batch_size=$6 --learning_rate=$7 --epoch=$8 --protocol=$9 2>$direrr/status-$10-$4-.log 1>$dir/output-$10-$4-.log &" &
