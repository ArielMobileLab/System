#!/bin/bash

function cleanup() {
    echo "Received Ctrl+C. Cleaning up..."

    pkill -TERM -f "CarlaUE4.sh"
    sleep 2s

    pkill -TERM -f "carla_ros_bridge"
    sleep 5s
    pkill -KILL -f "carla_ros_bridge" || echo "carla_ros_bridge process terminated successfully."
    
    rosnode kill /speedometer

    killall -9 python
    sleep 2s
    killall -9 python3

    exit 1
}

function free_port() {
    local port_to_free=2000
    local process_id=$(fuser $port_to_free/tcp 2>/dev/null)
    
    if [ -n "$process_id" ]; then
        echo "Process $process_id is using port $port_to_free. Terminating..."
        kill -9 $process_id
        echo "Process $process_id terminated."
    else
        echo "Port $port_to_free is not in use."
    fi
}

free_port

trap cleanup INT

"$HOME/Desktop/CARLA_0.9.13/CarlaUE4.sh" -windowed -ResX=640 -ResY=480 -benchmark -fps=10 &

sleep 11s

source /home/omer/carla-ros-bridge/catkin_ws/devel/setup.bash &&

roslaunch carla_ros_bridge First_Responders.launch town:=$1&

rosrun web_video_server web_video_server &

sleep 3s


run_python=python3


"$run_python" "$HOME/Desktop/API Addapter/Addapter.py" &


"$run_python" "$HOME/Desktop/CARLA_0.9.13/speed/speed.py" &
run_python=python
"$run_python" "$HOME/Desktop/API Addapter/RosToUDP.py" &


sleep 3s &&

run_python=python

"$run_python" "$HOME/Desktop/Autonomous Resope Unit/Arrow_Guide/Arrows_guide.py" $4 &



"$run_python" "$HOME/Desktop/Autonomous Resope Unit/RearVIew/Version_Ros_API_Work_For_Web.py" $4 &

"$run_python" "$HOME/Desktop/Autonomous Resope Unit/RearVIew/Rear_camera_API.py" $4 &

sleep 7s &&

"$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/First Responders/First responders/train/objects_train.py" &

sleep 2s &&



"$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/First Responders/First responders/train/Car_In_lane_train.py" &

sleep 2s &&

"$run_python" "$HOME/Desktop/API Addapter/phy.py" &

"$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/First Responders/First responders/train/Car_in_lane_train_ego_car.py" $7 & 



sleep 20s

"$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/First Responders/First responders/train/Car_In_lane_train_3.py"  & 



"$run_python" "$HOME/Desktop/API Addapter/Joy_addapter.py" &

"$run_python" "$HOME/Desktop/Comunication Unit/Latency.py" $5 &



wait

free_port

cleanup




