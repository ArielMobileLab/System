#!/bin/bash


#free_port 2000

#trap cleanup INT


#sleep 3s

export ROS_IP=10.20.0.1


roslaunch control streamer.launch &

sleep 5s &&



cd /opt/driveu/node/

./run_node &

sleep 10s &&

run_python=python

"$run_python" /home/omer/catkin_ws_streamer/src/control/src/speed/speed.py &

sleep 5s &&

curl http://127.0.0.1:8080/setBandwidth/1000


timestamp=$(date +\%Y-\%m-\%d_\%H-\%M-\%S)
# Create a new directory with the timestamp
output_directory="/home/omer/Desktop/Parent_experement/Logs_Parent/Real"

# Create the directory if it doesn't exist
mkdir -p "$output_directory"
timestamp=$(date +\%Y-\%m-\%d_\%H-\%M-\%S)
# Define the full path for the video file
output_file="$output_directory/Car_Video_Teleoperation_$timestamp.mp4"

# Run FFmpeg and save the video in the new directory
sleep 1s &&
ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0+0,0 \
    -f pulse -i default \
    "$output_file"

wait

