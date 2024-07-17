#!/bin/bash


#free_port 2000

#trap cleanup INT


#sleep 3s

roslaunch control streamer.launch &

sleep 3s &&

cd /opt/driveu/node/

./run_node &

sleep 3s &&

run_python=python

"$run_python" /home/omer/catkin_ws_streamer/src/control/src/speed/speed.py &

#sleep 1s &&
#"$run_python" "/home/omer/Desktop/Parent_experement/Voice_To_Json_PyAudio.py" &

wait


