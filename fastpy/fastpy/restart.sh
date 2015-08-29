port=$1
ps -ef | grep fastpy | grep $port | awk '{print $2}' | xargs -i{} kill -9 {}
nohup python fastpy.py $port > run.log 2>&1 &
