#!/bin/sh
dir=./stdout/
direrr=./stderr/ 

if [ "$9" = "ps" ] && [ "$1" = "0" ]
then
    rm -rf $direrr && mkdir $direrr
    rm -rf $dir && mkdir $dir
fi

echo "Running..."
    CUDA_VISIBLE_DEVICES=$4 python $10 --job_name=$9 --ps_list=$2 --wk_list=$3 --task_index=$1 --batch_size=$5 --learning_rate=$6 --epoch=$7 --protocol=$8 2>> $direrr/status-$9-$1-.log 1>> $dir/output-$9-$1-.log &

