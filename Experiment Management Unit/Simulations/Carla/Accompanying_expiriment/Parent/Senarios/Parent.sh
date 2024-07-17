#!/bin/bash


#free_port 2000

#trap cleanup INT


#sleep 3s

export ROS_IP=10.20.0.1

export ROS_MASTER_URI=http://10.20.0.164:11311


run_python=python

"$run_python" "/home/omer/Desktop/Parent_experement/Prent_Camera_v2.py" &


run_python=python3


"$run_python" "/home/omer/Desktop/CARLA_0.9.13/speed/speedParent.py" &


sleep 6s &&
"$run_python" "/home/omer/Desktop/Autonomous Response Unit/Map_Guide/Guide_Map_parent.py" $4 &


wait

#free_port 2000

#cleanup
