import carla
import json
from datetime import datetime
from collections import OrderedDict
import math
import time
import rospy
from sensor_msgs.msg import NavSatFix
import os
import sys

# Set the file name for JSON output
Agent_type = sys.argv[1]
#Agent_type = "test"
folder_path = "/home/omer/Desktop/Carla_Logs/Logs"
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = os.path.join(folder_path, 'Objects_{}_{}.json'.format(Agent_type, current_time))

simulation_time = 0.0
termination_data_added = False

# Initialize an empty set to keep track of written vehicles
written_vehicles = set()
encountered_static_objects = set()

write_to_json_flag = True
frame_id_counter = 0
flag = True

def generate_frame_id():
    global frame_id_counter
    frame_id_counter += 1
    return frame_id_counter

def write_to_json(data_dict, add_comma=True):
    global write_to_json_flag
    if write_to_json_flag:
        with open(file_name, 'a') as json_file:
            json.dump(data_dict, json_file, indent=2)  # Add indentation for better readability
            if add_comma:
                json_file.write(',\n')  # Add a comma and newline for proper JSON formatting
            else:
                json_file.write('\n')  # Add newline without a comma

def gnss_callback(data):
    global simulation_time
    # Process the GNSS data here
    # Example: Print the latitude and longitude
    simulation_time = data.header.seq * 0.033333335071821

def my_shutdown_callback():

    print("ROS node is shutting down. Performing cleanup...")
                        # Add the termination data only once
    global simulation_time
    timestamp = datetime.now().strftime('%H:%M:%S.%f')

    stop_data = OrderedDict()
    stop_data["Type"] = "Termination"
    stop_data["WorldTime"] = timestamp
    stop_data["SimulationTime"] = simulation_time
    stop_data["FrameID"] = generate_frame_id()
    stop_data["Reason"] = ""
    write_to_json(stop_data)
    close_json_file()  

def close_json_file():
    global flag
    flag  = False
    # Read the content of the JSON file
    with open(file_name, 'r') as json_file:
        content = json_file.read()

    # Remove trailing comma before closing brackets
    content = content.rstrip(', \t\n')  # Remove commas, spaces, tabs, and newlines at the end

    # Open the JSON file in write mode and write the modified content
    with open(file_name, 'w') as json_file:
        json_file.write(content)
        json_file.write('\n]}\n')  # Close the JSON array and file

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Get the world
world = client.get_world()

# Open the JSON file and start with {"Logs": [
with open(file_name, 'w') as json_file:
    json_file.write('{"Logs": [\n')

# Attach the callback function to the world's on_tick event
def on_world_tick(world_snapshot):
    global flag
    global simulation_time
    global actor_data
    #simulation_time += 0.033333335071821  # Assuming a fixed frame rate of approximately 30 FPS
    global termination_data_added
    

    if flag:
        for actor_snapshot in world_snapshot:
            actor_id = actor_snapshot.id
            actor = world.get_actor(actor_id)

            if actor:
                actor_name = str(actor.type_id) + " " + str(actor_id)
                timestamp = datetime.now().strftime('%H:%M:%S.%f')

                if actor.type_id.startswith('walker'):
                    actor_info = OrderedDict()
                    actor_info["Type"] = "GPS"
                    actor_info["Name"] = actor_name
                    actor_info["WorldTime"] = timestamp
                    actor_info["SimulationTime"] = simulation_time
                    actor_info["FrameID"] = generate_frame_id()
                    actor_info["SimulationPosition"] = {
                        "x": str(actor.get_location().x),
                        "y": str(actor.get_location().y),
                        "z": str(actor.get_location().z)
                    }
                    carla_location = carla.Location(actor.get_location().x, actor.get_location().y, actor.get_location().z)
                    world_map = world.get_map()
                    geolocation = world_map.transform_to_geolocation(carla_location)
                    actor_info["Longitude"] = str(geolocation.longitude)
                    actor_info["Latitude"] = str(geolocation.latitude)
                    actor_info["Altitude"] = str(geolocation.altitude)
  
                    write_to_json(actor_info)

                elif actor.type_id.startswith('vehicle') and not actor.attributes.get('role_name', '') == 'ego_vehicle':
                    if actor.type_id in ['vehicle.dodge.charger_police', 'vehicle.audi.tt']:
                        if actor.type_id not in written_vehicles:
                            # Write only during the first occurrence of the vehicle
                            actor_info = OrderedDict()
                            actor_info["Type"] = "GPS"
                            actor_info["Name"] = actor_name
                            actor_info["WorldTime"] = timestamp
                            actor_info["SimulationTime"] = simulation_time
                            actor_info["FrameID"] = generate_frame_id()
                            actor_info["SimulationPosition"] = {
                                "x": str(actor.get_location().x),
                                "y": str(actor.get_location().y),
                                "z": str(actor.get_location().z)
                            }

                            carla_location = carla.Location(actor.get_location().x, actor.get_location().y, actor.get_location().z)
                            world_map = world.get_map()
                            geolocation = world_map.transform_to_geolocation(carla_location)
                            actor_info["Longitude"] = str(geolocation.longitude)
                            actor_info["Latitude"] = str(geolocation.latitude)
                            actor_info["Altitude"] = str(geolocation.altitude)

                            write_to_json(actor_info)

                            written_vehicles.add(actor.type_id)  # Mark as written
                    else:
                        # Write information about other vehicles
                        actor_info = OrderedDict()
                        actor_info["Type"] = "GPS"
                        actor_info["Name"] = actor_name
                        actor_info["WorldTime"] = timestamp
                        actor_info["SimulationTime"] = simulation_time
                        actor_info["FrameID"] = generate_frame_id()
                        actor_info["SimulationPosition"] = {
                            "x": str(actor.get_location().x),
                            "y": str(actor.get_location().y),
                            "z": str(actor.get_location().z)
                        }
                        actor_transform = actor.get_transform()
                        actor_info["Orientation"] = {
                            "x": str(actor_transform.rotation.pitch),
                            "y": str(actor_transform.rotation.yaw),
                            "z": str(actor_transform.rotation.roll)
                        }
                        carla_location = carla.Location(actor.get_location().x, actor.get_location().y, actor.get_location().z)
                        world_map = world.get_map()
                        geolocation = world_map.transform_to_geolocation(carla_location)
                        actor_info["Longitude"] = str(geolocation.longitude)
                        actor_info["Latitude"] = str(geolocation.latitude)
                        actor_info["Altitude"] = str(geolocation.altitude)
            
                        actor_info["Speed"] = math.sqrt(actor.get_velocity().x ** 2 + actor.get_velocity().y ** 2)
                        #actor_info["Acceleration"] = str(actor.get_acceleration().x)
			actor_info["Acceleration"] = {
                            "x": str(actor.get_acceleration().x),
                            "y": str(actor.get_acceleration().y),
                            "z": str(actor.get_acceleration().z)
                        }
                        write_to_json(actor_info)

                elif actor.type_id.startswith('static.prop.streetbarrier'):
                    # Check if the static object has been encountered before
                    actor_tuple = (actor.type_id, actor_id)
                    if actor_tuple not in encountered_static_objects:
                        # Handle static objects like "static.prop.streetbarrier"
                        static_info = OrderedDict()
                        static_info["Type"] = "StaticObject"
                        static_info["Name"] = actor_name
                        static_info["WorldTime"] = timestamp
                        static_info["SimulationTime"] = simulation_time
                        static_info["Position"] = {
                            "x": str(actor.get_location().x),
                            "y": str(actor.get_location().y),
                            "z": str(actor.get_location().z)
                        }
                        carla_location = carla.Location(actor.get_location().x, actor.get_location().y, actor.get_location().z)
                        world_map = world.get_map()
                        geolocation = world_map.transform_to_geolocation(carla_location)
                        static_info["Longitude"] = str(geolocation.longitude)
                        static_info["Latitude"] = str(geolocation.latitude)
                        static_info["Altitude"] = str(geolocation.altitude)
                        
                        write_to_json(static_info)

                        encountered_static_objects.add(actor_tuple)
 

# Initialize ROS node
if __name__ == '__main__':
    rospy.init_node('carla_data_logger', anonymous=True)
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, gnss_callback)

    # Attach the callback function to the world's on_tick event
    world.on_tick(lambda snapshot: on_world_tick(snapshot))
    rospy.on_shutdown(my_shutdown_callback)
    try:
        while not rospy.is_shutdown():
            time.sleep(1)  # Sleep for a short duration to avoid high CPU usage
    except KeyboardInterrupt:
        # Close the JSON array when the script is interrupted
        with open(file_name, 'a') as json_file:
            json_file.write('\n]}\n')
