#!/bin/bash

killall -9 python
killall -9 CarlaUE4 CarlaUE4.sh || echo "CarlaUE4 was not running."


# Function to perform cleanup on Ctrl+C
function cleanup() {
    echo "Received Ctrl+C. Cleaning up..."
    
    # Add any cleanup actions here
    ( killall -9 CarlaUE4 CarlaUE4.sh 2>&1 ) > /dev/null

    pkill -f "roslaunch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch"
    pkill -f "$run_python $HOME/cognata_sdk_ros1_ws/src/cognata_sdk/src/N_FaceFunction19.9.py"
    pkill -f "$run_python" "$HOME/Desktop/CARLA_0.9.13/speed/speed.py"  
    pkill -f "$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Spatial/Static_Objects.py" 
    pkill -f "$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Spatial/Finish/Walkers.py" 
    pkill -f "$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Spatial/Finish/Cars_Traffic_Lights.py" 
    # Exit the script
    exit 1
}

# Trap Ctrl+C and call the cleanup function
trap cleanup INT


# Function to free the port of the server of carla
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

# Free port 2000
free_port 2000

# Kill existing Python and Carla processes
killall -9 python
( killall -9 CarlaUE4 CarlaUE4.sh 2>&1 ) > /dev/null
echo "Killed existing Python and Carla processes."

clear


run_python=python3
town=Town03;

case $1 in
    Town01Restaurant)
        scenario=Town01Restaurant
        town=Town01
        ;;
    Town03GasStation)
        scenario=Town03GasStation
        town=Town03
        ;;
    Town03TrainTrack)
        scenario=Town03TrainTrack
        town=Town03
        ;;
    Town04ParkingLot)
        scenario=Town04ParkingLot
        town=Town04
        ;;
    Town07Farm)
        scenario=Town07Farm
        town=Town07
        ;;
    *)
        scenario=Town03GasStation
        town=Town03
        ;;


esac

"$HOME/Desktop/CARLA_0.9.13/CarlaUE4.sh" "/Game/Carla/Maps/Town05" > log_server.txt &
/home/omer/Desktop/Carla_Logs
sleep 6s
xdotool windowminimize "$(wmctrl -l | grep "CarlaUE4" | cut -d ' ' -f1)"
 sleep 6s
 source /home/omer/carla-ros-bridge/catkin_ws/devel/setup.bash &&

 # $1 give the first argumnet that responsible for the town chose as we able to see in the agrumnet of the lunch file
roslaunch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch town:=$1&

 "$run_python" "$HOME/Desktop/API Addapter/Addapter.py" &
 "$run_python" "$HOME/Desktop/CARLA_0.9.13/speed/speed.py"&

 # $3 give the argumnet that responsible for the objects of the senario 
 if [ "$3" == "Spatial" ]; then
 sleep 6s &&

 run_python=python #this script run with python and not python 3 like the face script
  # $2 give the argumnet that responsible for the Face Agent 
 
 if [ "$2" == "Face" ] || [ "$2" = "Color" ] ; then
 "$run_python" "$HOME/Desktop/Autonomous Resope Unit/Avatar_Guide/Face_Last_Version.py" $2&
 fi

 "$run_python" "$HOME/Desktop/Autonomous Resope Unit/Arrow_Guide/Arrows_guide.py" $4 &
 "$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Spatial/Finish/Static_Objects.py" &
 "$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Spatial/Finish/Walkers.py" &
 "$run_python" "$HOME/Desktop/CARLA_0.9.13/PythonAPI/examples/Map_objects/Spatial/Finish/Cars_Traffic_Lights.py" &
 "$run_python" "$HOME/Desktop/Carla_Logs/Ego_Car_log.py" &


 wait
 fi

killall -9 python
( killall -9 CarlaUE4 CarlaUE4.sh 2>&1 ) > /dev/null

