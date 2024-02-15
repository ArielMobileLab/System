import socket
import struct
import rospy
from sensor_msgs.msg import NavSatFix

MatLabIP = "10.20.0.96"
MatLabPort = 12355
bufferSize = 2048

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Initialize a global variable

def time(data):

    # Increment the global_sequence each time the function is called


    # Extract data for the selected measurements
    time = [data.header.seq * 0.033333335071821,1.0]

    # Pack the data using the format string
    packed_data = struct.pack(f"{len(time)}d", *time)


    # Send the packed data to the specified IP and port
    UDPServerSocket.sendto(packed_data, (MatLabIP, MatLabPort))

def main():
    rospy.init_node('RosToUDP')
    
    # Subscribe to the GNSS topic
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, time)
    
    rospy.spin()

if __name__ == '__main__':
    main()
