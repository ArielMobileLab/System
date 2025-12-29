import carla
import time
import math
import threading
import xml.etree.ElementTree as ET
import socket


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


def send_udp_message_to_brain(challenge_name, object_id, data_dict):
    # Compose message as: "ConditionName | ObjectID: id | key1: val1 | key2: val2 ..."
    parts = ["{} | Object: {}".format(challenge_name, object_id)]
    for k, v in data_dict.items():
        if isinstance(v, (int, float)):
            parts.append("{}: {:.2f}".format(k, v))
        else:
            parts.append("{}: {}".format(k, v))
    message = " | ".join(parts)
    # Debug print
    print("[SEND UDP] {}".format(message))
    UDPServerSocket.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))


def monitor_challenge(object_id, measures, interval, challenge_name, world):
    ego_actor = world.get_actor(229)  # Ego vehicle with ID 229
    actor = world.get_actor(object_id)
    print(challenge_name)
    if not actor:
        print("[ERROR][{}] Object with ID {} not found.".format(challenge_name, object_id))
        return

    actor_type = actor.type_id
    print("[START][{}] Monitoring object {} ({}) | Measures: {} | Interval: {}s".format(
        challenge_name, object_id, actor_type, measures, interval))
    

    while True:
        output = {}
        try:
            location = actor.get_location()
        except:
            location = None

        try:
            velocity = actor.get_velocity()
        except:
            velocity = None

        try:
            rotation = actor.get_transform().rotation
        except:
            rotation = None

        try:
            acceleration = actor.get_acceleration() 
        except:
            acceleration = None    

        try:
            angular_velocity = actor.get_angular_velocity()
        except:
            angular_velocity = None

        for measure in measures:

            if measure == "velocity.x" and velocity:
                output[measure] = velocity.x
            elif measure == "velocity.y" and velocity:
                output[measure] = velocity.y
            elif measure == "velocity.z" and velocity:
                output[measure] = velocity.z
            elif measure == "location.x":
                output[measure] = location.x
            elif measure == "location.y":
                output[measure] = location.y
            elif measure == "location.z":
                output[measure] = location.z
            elif measure == "rotation.pitch" and rotation:
                output[measure] = rotation.pitch
            elif measure == "rotation.yaw" and rotation:
                output[measure] = rotation.yaw
            elif measure == "rotation.roll" and rotation:
                output[measure] = rotation.roll
            elif measure == "angular_velocity.x" and angular_velocity:
                output[measure] = angular_velocity.x
            elif measure == "angular_velocity.y" and angular_velocity:
                output[measure] = angular_velocity.y
            elif measure == "angular_velocity.z" and angular_velocity:
                output[measure] = angular_velocity.z
            elif measure == "acceleration.x" and acceleration:
                output[measure] = acceleration.x
            elif measure == "acceleration.y" and acceleration:
                output[measure] = acceleration.y
            elif measure == "acceleration.z" and acceleration:
                output[measure] = acceleration.z
            elif measure == "actor_active_distance":
                location_ego_car = ego_actor.get_location()
                output[measure] = location_ego_car.distance(location)    
            elif measure == "trafficlightstate":
                output[measure] = actor.state.name

            else:
                output[measure] = "[UNSUPPORTED or NOT AVAILABLE]"

        send_udp_message_to_brain(challenge_name, actor_type, output)

        time.sleep(interval)


def monitor_from_xml(xml_path, client, world):
    tree = ET.parse(xml_path)
    root = tree.getroot()   # Now this will be <Challenges>
    threads = []

    # Iterate over all children of <Challenges>: <Challenge1>, <Challenge2>, ...
    for challenge_elem in root.findall("./*"):
        object_id = int(challenge_elem.findtext("ObjectID", 0))
        interval = float(challenge_elem.findtext("IntervalSeconds", 1))

        measures = []
        for m in challenge_elem.findall(".//Measure"):
            if m.text:
                measures.append(m.text.strip().lower())

        challenge_name = challenge_elem.tag   # Example: "Challenge1"

        # Start thread
        t = threading.Thread(
            target=monitor_challenge,
            args=(object_id, measures, interval, challenge_name, world)
        )
        t.daemon = True
        t.start()
        threads.append(t)

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")


def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    monitor_from_xml("Challenges.xml", client, world)


if __name__ == "__main__":
    main()
