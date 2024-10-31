#!/bin/bash

function cleanup() {
    echo "Received Ctrl+C. Cleaning up..."
    killall -9 python
    sleep 2s
    killall -9 python3
    sleep 2s
    #killall -9 CarlaUE4 CarlaUE4.sh || echo "CarlaUE4 was not running."
    sleep 2s
    #pkill -15 -f "roslaunch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch"
    sleep 2s
    #pkill -9 -f "roslaunch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch"

    # Terminate carla_ros_bridge process
    pkill -TERM -f "carla_ros_bridge"

    # Wait for a short period for the process to respond to SIGTERM
    sleep 10

    # If the process is still running, escalate to SIGKILL
    pkill -KILL -f "carla_ros_bridge" || echo "carla_ros_bridge process terminated successfully."

    killall -9 python
    sleep 2s
    killall -9 python3
    sleep 2s

    # Add cleanup tasks for other processes if needed

    exit 1
}

function free_port() {
    local port_to_free=$1
    local process_id=$(fuser $port_to_free/tcp 2>/dev/null)
    
    if [ -n "$process_id" ]; then
        echo "Process $process_id is using port $port_to_free. Terminating..."
        kill -9 $process_id
        echo "Process $process_id terminated."
    else
        echo "Port $port_to_free is not in use."
    fi
}

free_port 2000

trap cleanup INT



"$HOME/Desktop/CARLA_0.9.13/CarlaUE4.sh" -windowed -ResX=640 -ResY=480 -benchmark -fps=20 &

sleep 11s

source /home/omer/carla-ros-bridge/catkin_ws/devel/setup.bash &&


roslaunch carla_ros_bridge Train_Parent.launch town:=$1&

sleep 3s


run_python=python3

"$run_python" "$HOME/Desktop/API Addapter/Addapter.py" &
"$run_python" "$HOME/Desktop/CARLA_0.9.13/speed/speed.py" &
run_python=python
"$run_python" "$HOME/Desktop/API Addapter/RosToUDP.py" &

sleep 6s &&

run_python=python


"$run_python" "$HOME/Desktop/Autonomous Resope Unit/Arrow_Guide/Arrows_guide.py" $4 &


sleep 1s &&



"$run_python" "$HOME/Desktop/Autonomous Resope Unit/RearVIew/Front_Camera_API_Parent_V2.py.py" $4 &


sleep 3s &&

"$run_python" "$HOME/Desktop/API Addapter/phy.py" 

#"$run_python" "$HOME/Desktop/Carla_Logs/Ego_Car_log.py" $2 &
#"$run_python" "$HOME/Desktop/Carla_Logs/Objects_log.py" $2 &

"$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Parent/Mordechai/Train_Objects.py" &


sleep 6s &&

wait

free_port 2000

cleanup
