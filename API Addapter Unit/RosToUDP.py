import socket
import struct
import rospy
import carla
from sensor_msgs.msg import NavSatFix
import os
import sys

MatLabIP = "10.20.0.188"
MatLabPort = 12355
bufferSize = 2048

Senario_Type = sys.argv[1]
Senario_Type = int(Senario_Type)


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

simulation_time_ros = 0.0

# Initialize a global variable

def on_world_tick(world_snapshot):

    global simulation_time_ros

    simulation_time = world_snapshot.timestamp.elapsed_seconds

    data_Send = [simulation_time_ros, simulation_time, Senario_Type]

    # Pack the data using the format string
    packed_data = struct.pack("%dd" % len(data_Send), *data_Send)


    # Send the packed data to the specified IP and port
    UDPServerSocket.sendto(packed_data, (MatLabIP, MatLabPort))



def simulation_time_UDP(data):

    global simulation_time_ros

    # Ros time
    simulation_time_ros = data.header.seq * 0.033333335071821


def main():
    rospy.init_node('RosToUDP')
    
    world.on_tick(lambda snapshot: on_world_tick(snapshot))
    # Subscribe to the GNSS topic
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, simulation_time_UDP)
    
    rospy.spin()

if __name__ == '__main__':
    main()
