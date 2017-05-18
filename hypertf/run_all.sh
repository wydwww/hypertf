#!/bin/bash  

LOC="/home/ywang/hypertf/hypertf"
SOURCE_CMD="source /home/jiacheng/pyenv/tf_roc2/bin/activate"
dir=./stdout/
direrr=./stderr/

echo $@

ssh $3 "$SOURCE_CMD && cd $LOC && CUDA_VISIBLE_DEVICES=$5 python $11 --job_name=$10 --ps_list=$1 --wk_list=$2 --task_index=$4 --batch_size=$6 --learning_rate=$7 --epoch=$8 --protocol=$9 2>$direrr/status-$10-$4-.log 1>$dir/output-$10-$4-.log &" &

