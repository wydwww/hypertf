#!/bin/bash  

ssh $3 "source /home/jiacheng/pyenv/tf_dis/bin/activate && cd /home/ywang/hypertf/hypertf && sh run1.sh $4 $1 $2 $5 $6 $7 $8 $9 $10 $11" 
