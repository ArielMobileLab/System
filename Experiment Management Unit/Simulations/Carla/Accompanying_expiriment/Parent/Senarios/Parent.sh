#!/bin/bash


#free_port 2000

#trap cleanup INT



#"$HOME/Desktop/CARLA_0.9.13/CarlaUE4.sh" &

#sleep 11s

#source /home/omer/carla-ros-bridge/catkin_ws/devel/setup.bash &&


#roslaunch carla_ros_bridge Train_Corraction.launch town:=$1&

#sleep 3s

export ROS_IP=10.20.0.1

export ROS_MASTER_URI=http://10.20.0.180:11311


run_python=python

"$run_python" "/home/omer/Desktop/Parent_experement/Prent_Camera_v2.py" &
#"$run_python" "/home/omer/Desktop/Parent_experement/Camera_amorgency0.py" &
sleep 1s &&
#"$run_python" "/home/omer/Desktop/Parent_experement/Camera_amorgency1.py" &


run_python=python3

#"$run_python" "/home/omer/Desktop/API Addapter Unit/Addapter.py" &
"$run_python" "/home/omer/Desktop/CARLA_0.9.13/speed/speedParent.py" &
#"$run_python" "/home/omer/Desktop/API Addapter Unit/RosToUDP.py" &

sleep 6s &&
"$run_python" "/home/omer/Desktop/Autonomous Response Unit/Map_Guide/Arrow_Guide_With_C_Parent_Side.py" $4 &

sleep 1s &&
"$run_python" "/home/omer/Desktop/Parent_experement/Voice_To_Json_PyAudio.py" $2 &

timestamp=$(date +\%Y-\%m-\%d_\%H-\%M-\%S)
# Create a new directory with the timestamp
output_directory="/home/omer/Desktop/Parent_experement/Logs_Parent/Far"

# Create the directory if it doesn't exist
mkdir -p "$output_directory"
timestamp=$(date +\%Y-\%m-\%d_\%H-\%M-\%S)
# Define the full path for the video file
output_file="$output_directory/Parent_Far_Physiological_$timestamp.mp4"

# Run FFmpeg and save the video in the new directory
sleep 1s &&
ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0+0,0 \
    -f pulse -i default \
    "$output_file"


#sleep 1s &&
#ffmpeg -video_size 1920x1080 -framerate 15 -f x11grab -i :0.0+0,0 /home/omer/Desktop/Parent_experement/Logs/Far/Parent_Far_$(date +\%Y-\%m-\%d_\%H-\%M-\%S).mp4

#run_python=python #this script run with python and not python 3 like the face script

  # $2 give the argumnet that responsible for the Face Agent 
 

#"$run_python" "$HOME/Desktop/Autonomous Resope Unit/RearVIew/Rearview_Mirror.py" &



wait

#free_port 2000

#cleanup
