#!/bin/bash


#free_port 2000

#trap cleanup INT



#"$HOME/Desktop/CARLA_0.9.13/CarlaUE4.sh" &

#sleep 11s

#source /home/omer/carla-ros-bridge/catkin_ws/devel/setup.bash &&


#roslaunch carla_ros_bridge Train_Corraction.launch town:=$1&

#sleep 3s

export ROS_IP=10.20.0.1

export ROS_MASTER_URI=http://10.20.0.164:11311


run_python=python

"$run_python" "/home/omer/Desktop/Parent_experement/Prent_Camera_v2.py" &


run_python=python3

#"$run_python" "/home/omer/Desktop/API Addapter Unit/Addapter.py" &
"$run_python" "/home/omer/Desktop/CARLA_0.9.13/speed/speedParent.py" &
#"$run_python" "/home/omer/Desktop/API Addapter Unit/RosToUDP.py" &

sleep 6s &&
"$run_python" "/home/omer/Desktop/Autonomous Response Unit/Map_Guide/Guide_Map_parent.py" $4 &

#sleep 1s &&
#"$run_python" "/home/omer/Desktop/Parent_experement/Voice_To_Json_PyAudio.py" &

#run_python=python #this script run with python and not python 3 like the face script
  # $2 give the argumnet that responsible for the Face Agent 
 

#"$run_python" "$HOME/Desktop/Autonomous Resope Unit/RearVIew/Rearview_Mirror.py" &



wait

#free_port 2000

#cleanup
