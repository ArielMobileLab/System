
# Code that generate log of the Ego car.
#   - Refernce to snap function in caral, link: https://carla.readthedocs.io/en/latest/python_api/#carla.WorldSnapshot


import carla
import json
from datetime import datetime
from collections import OrderedDict
import math
import time
import rospy
from sensor_msgs.msg import NavSatFix
from carla_msgs.msg import CarlaCollisionEvent 
import sys
import os


# Set the file name for JSON output
Agent_type = sys.argv[1]
Map_type = sys.argv[2]
#Agent_type = "Test"
#Map_type = "Test"
folder_path = "/home/omer/Desktop/Carla_Logs/Logs"
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = os.path.join(folder_path, 'EgoCar_{}_{}.json'.format(Agent_type, current_time))
SimulationTime_Ros = 0.0
SimulationTime = 0.0
stop_write = False
colition_flag = False
frame_id = 0.0
No_need_for_my_shutdown_callback = False


termination_data_added = False

# Initialize an empty set to keep track of written vehicles
written_vehicles = set()
write_to_json_flag = True
frame_id_counter = 0


# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Get the world
world = client.get_world()


# Start the JSON file
with open(file_name, 'w') as json_file:
    json_file.write('{"Logs": [\n')


def generate_frame_id():
    global frame_id_counter
    frame_id_counter += 1
    return frame_id_counter


def gnss_callback(data):
    global SimulationTime_Ros
    # Process the GNSS data here
    # Example: Print the latitude and longitude
    SimulationTime_Ros = data.header.seq * 0.033333335071821



def my_shutdown_callback():
    global No_need_for_my_shutdown_callback
    global stop_write
    global SimulationTime
    if No_need_for_my_shutdown_callback ==  False:
        if stop_write == False:
            stop_write = True
            timestamp = datetime.now().strftime('%H:%M:%S.%f')


            stop_data = OrderedDict()
            stop_data["Type"] = "Termination"
            stop_data["WorldTime"] = timestamp
            stop_data["SimulationTime"] = SimulationTime
            stop_data["FrameID"] = FrameID
            stop_data["Reason"] = "operetor_stop"

            print("Writing stop data to JSON...")
            write_to_json(stop_data)
            close_json_file()
            



def write_to_json(data_dict, add_comma=True):
    if write_to_json_flag:
        with open(file_name, 'a') as json_file:
            json.dump(data_dict, json_file, indent=2)  # Add indentation for readability
            if add_comma:
                json_file.write(',\n')
            else:
                json_file.write('\n')


def collision_callback(data):
    global colition_flag 
    timestamp = datetime.now().strftime('%H:%M:%S.%f')

    if colition_flag == False:

        colition_flag = True

        actor_id = data.other_actor_id

        client = carla.Client('127.0.0.1', 2000)
        world = client.get_world()  # Make sure to obtain the actual world instance
        actor = world.get_actor(actor_id)
        world_snapshot = world.wait_for_tick()
        simulation_time_colition = world_snapshot.timestamp.elapsed_seconds
        frame_id_coliton = world_snapshot.timestamp.frame

# Get the current world snapshot

# Retrieve simulation time

        # Check if the actor is valid
        if actor:
            actor_info =  actor
            actor_info = str(actor)
            start_index = actor_info.find("type=") + len("type=")
            end_index = actor_info.find(")", start_index)
            actor_name = actor_info[start_index:end_index].strip()
            

        else:
                    actor_name = "Unknown"

        SimulationTime = world_snapshot.timestamp.elapsed_seconds
        FrameID = world_snapshot.timestamp.frame
        stop_data = OrderedDict()
        stop_data["Type"] = "Termination"
        stop_data["WorldTime"] = timestamp
        stop_data["SimulationTime"] = simulation_time_colition
        stop_data["FrameID"] = frame_id_coliton
        stop_data["Reason"] = "Crash" + "-" + actor_name
        write_to_json(stop_data, add_comma=False)


        close_json_file()


def close_json_file():
    global stop_write
    with open(file_name, 'r') as json_file:
        content = json_file.read()
    content = content.rstrip(', \t\n')  # Remove trailing commas
    with open(file_name, 'w') as json_file:
        json_file.write(content)
        json_file.write('\n]}')  # Close the JSON array
        stop_write = True


def on_world_tick(world_snapshot):
    
    global stop_write
    global frame_id_counter
    global SimulationTime_Ros
    global SimulationTime
    global FrameID
    global No_need_for_my_shutdown_callback

    termination_condition_met = False  # Flag to track if termination condition has been met

    for actor_snapshot in world_snapshot:  # This should loop through actors
        actor_id = actor_snapshot.id
        actor = world.get_actor(actor_id)

        if stop_write == False:
            if colition_flag == False:

                # Check if the actor is the ego vehicle
                if actor.attributes.get('role_name', '') == 'ego_vehicle':
                    timestamp = datetime.now().strftime('%H:%M:%S.%f')
                    SimulationTime = world_snapshot.timestamp.elapsed_seconds
                    FrameID = world_snapshot.timestamp.frame

                    actor_info = OrderedDict()
                    actor_info["Type"] = "GPS"
                    actor_info["WorldTime"] = timestamp
                    actor_info["SimulationTime_Ros"] = SimulationTime_Ros
                    actor_info["FrameID_Ros"] = generate_frame_id()
                    actor_info["SimulationTime"] = SimulationTime
                    actor_info["FrameID"] = FrameID
                    actor_info["SimulationPosition"] = {
                        "x": actor.get_location().x,
                        "y": actor.get_location().y,
                        "z": actor.get_location().z
                    }

                    # Handle First_Response end of the simulation
                    if (Map_type == "First_Response_Tele_assist" or Map_type == "First_Response_Tele_driving") and not termination_condition_met:
                        if actor.get_location().x > -180.0:
                            print("closing JSON file.")
                            actor_info = OrderedDict()
                            actor_info["Type"] = "Termination"
                            actor_info["WorldTime"] = timestamp
                            actor_info["SimulationTime"] = SimulationTime
                            actor_info["FrameID"] = FrameID
                            actor_info["Reason"] = "End of the simulation"
                            write_to_json(actor_info)
                            close_json_file()  # Close the JSON file when the condition is met
                            No_need_for_my_shutdown_callback = True
                            termination_condition_met = True  # Set flag to True, indicating termination condition met
                            return  # Exit function

                    # Handle Guide_Parent map type
                    elif (Map_type == "Guide_Parent_no_PD" or Map_type == "Guide_Parent_PD") and not termination_condition_met:
                        if 90.128  < actor.get_location().y < 116.1248 and 88.2840 < actor.get_location().x < 92.3620:
                            print("closing JSON file.")
                            actor_info = OrderedDict()
                            actor_info["Type"] = "Termination"
                            actor_info["WorldTime"] = timestamp
                            actor_info["SimulationTime"] = SimulationTime
                            actor_info["FrameID"] = FrameID
                            actor_info["Reason"] = "End of the simulation"
                            write_to_json(actor_info)
                            close_json_file()  # Close the JSON file when the condition is met
                            No_need_for_my_shutdown_callback = True
                            termination_condition_met = True  # Set flag to True, indicating termination condition met
                            return  # Exit function

                    # If termination conditions are not met, continue with regular processing
                    if not termination_condition_met:
                        world_map = world.get_map()
                        carla_location = carla.Location(actor.get_location().x, actor.get_location().y, actor.get_location().z)
                        geolocation = world_map.transform_to_geolocation(carla_location)
                        actor_info["Latitude"] = geolocation.latitude
                        actor_info["Longitude"] = geolocation.longitude
                        actor_info["Altitude"] = geolocation.altitude
                        actor_transform = actor.get_transform()
                        actor_info["Orientation"] = {
                            "x": actor_transform.rotation.pitch,
                            "y": actor_transform.rotation.yaw,
                            "z": actor_transform.rotation.roll
                        }
                        actor_info["Speed"] = math.sqrt(actor.get_velocity().x ** 2 + actor.get_velocity().y ** 2) * 3.6
                        actor_info["Acceleration"] = {
                            "x": actor.get_acceleration().x,
                            "y": actor.get_acceleration().y,
                            "z": actor.get_acceleration().z
                        }
                        actor_info["VelocityLocal3D"] = {"x": actor.get_velocity().x, "y": actor.get_velocity().x, "z": actor.get_velocity().x}
                        angular_velocity = actor.get_angular_velocity()
                        actor_info["AngularAccelerationLocal3D"] = {"x": angular_velocity.x, "y": angular_velocity.y, "z": angular_velocity.z}

                        write_to_json(actor_info)

                        actor_info = OrderedDict()
                        actor_info["Type"] = "Car_Telemetries"
                        actor_info["WorldTime"] = timestamp
                        actor_info["SimulationTime_Ros"] = SimulationTime_Ros
                        actor_info["FrameID_Ros"] = generate_frame_id()
                        actor_info["SimulationTime"] = SimulationTime
                        actor_info["FrameID"] = FrameID
                        actor_info["Speed"] = math.sqrt(actor.get_velocity().x ** 2 + actor.get_velocity().y ** 2) * 3.6
                        actor_info["Acceleration"] = actor.get_acceleration().x
                        control = actor.get_control()
                        actor_info["SteeringAngle"] = control.steer
                        actor_info["Brake"] = control.brake
                        actor_info["Gas"] = control.throttle
                        vehicle = client.get_world().get_actor(actor_id)
                        gear = vehicle.get_control().gear
                        actor_info["Gear"] = gear

                        write_to_json(actor_info)


   
# Initialize ROS node
if __name__ == '__main__':

    rospy.init_node('carla_data_logger', anonymous=True)
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, gnss_callback)
    rospy.Subscriber("/carla/ego_vehicle/collision", CarlaCollisionEvent, collision_callback)

    world.on_tick(lambda snapshot: on_world_tick(snapshot))
    
    rospy.on_shutdown(my_shutdown_callback)

    try:
        while not rospy.is_shutdown():
            time.sleep(0.5)
    except KeyboardInterrupt:
        with open(file_name, 'a') as json_file:
            json_file.write('\n]}')  # Close the JSON array when interrupted
