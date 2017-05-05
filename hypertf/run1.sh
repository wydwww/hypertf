#!/bin/sh
# run like sh run_test2.sh <index>
dir=./stdout/
direrr=./stderr/ 

if [ "$1" = "0" ]
then
    rm -rf $direrr && mkdir $direrr
    rm -rf $dir && mkdir $dir
fi

echo "Running..."
if [ "$1" = "0" ]
then
    CUDA_VISIBLE_DEVICES=$4 python complex_MNIST4.py --job_name="ps" --ps_list=$2 --wk_list=$3 --task_index=$1 2>> $direrr/status$1 1>> $dir/output-ps$1 &
elif [ "$1" = "1" ]
then
    CUDA_VISIBLE_DEVICES=$4 python complex_MNIST4.py --job_name="worker" --ps_list=$2 --wk_list=$3 --task_index=0 2>> $direrr/status$1 1>> $dir/output-wk$1 &
elif [ "$1" = "2" ] 
then 
    CUDA_VISIBLE_DEVICES=$4 python complex_MNIST4.py --job_name="worker" --ps_list=$2 --wk_list=$3 --task_index=1 2>> $direrr/status$1 1>> $dir/output-wk$1 &
elif [ "$1" = "3" ] 
then     
    CUDA_VISIBLE_DEVICES=$4 python complex_MNIST4.py --job_name="worker" --ps_list=$2 --wk_list=$3 --task_index=2 2>> $direrr/status$1 1>> $dir/output-wk$1 &
fi

