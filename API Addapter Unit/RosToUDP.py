import socket
import struct
import rospy
import carla
from sensor_msgs.msg import NavSatFix

# Define two IP addresses
MatLabIP = "10.20.0.188"
GUI_tele_assist_IP = "10.20.0.184"
Port = 12355
bufferSize = 2048

# Create the UDP socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Connect to Carla
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

simulation_time_ros = 0.0

def on_world_tick(world_snapshot):
    global simulation_time_ros
    simulation_time = world_snapshot.timestamp.elapsed_seconds
    time = [simulation_time_ros, simulation_time]

    # Pack the data
    packed_data = struct.pack("%dd" % len(time), *time)

    # Send the packed data to both IP addresses
    UDPServerSocket.sendto(packed_data, (MatLabIP, Port))
    UDPServerSocket.sendto(packed_data, (GUI_tele_assist_IP, Port))

def simulation_time_UDP(data):
    global simulation_time_ros
    simulation_time_ros = data.header.seq * 0.033333335071821

def main():
    rospy.init_node('RosToUDP')
    world.on_tick(lambda snapshot: on_world_tick(snapshot))
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, simulation_time_UDP)
    rospy.spin()

if __name__ == '__main__':
    main()
