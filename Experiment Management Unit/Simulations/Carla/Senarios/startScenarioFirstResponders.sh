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

"$HOME/Desktop/CARLA_0.9.13/CarlaUE4.sh" -windowed -ResX=640 -ResY=480 -benchmark -fps=20 &

sleep 11s

source /home/omer/carla-ros-bridge/catkin_ws/devel/setup.bash &&

roslaunch carla_ros_bridge First.launch town:=$1&

#sleep 3s

#run_python=python3


#"$run_python" "/home/omer/Desktop/API Addapter Unit/Addapter.py" &
#"$run_python" "/home/omer/Desktop/CARLA_0.9.13/speed/speed.py" &
#"$run_python" "/home/omer/Desktop/API Addapter Unit/RosToUDP.py" &




#sleep 1s &&
#"$run_python" "/home/omer/Desktop/Ego Car Logs/Carla logs/Objects_log.py" $2 &
#"$run_python" "/home/omer/Desktop/Ego Car Logs/Carla logs/Ego_Car_log.py" $2 &
#sleep 2s &&

#"$run_python" "/home/omer/Desktop/API Addapter Unit/phy.py" 


wait

free_port

cleanup
