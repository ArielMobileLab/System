#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry



def imu_recive(data):
    global_pipe_IMU.publish(data)

def GPS_recive(data):
    global_pipe_GPS.publish(data)

def odometry_recive(data):
    global_pipe_Odomerty.publish(data)

def main():
    rospy.init_node('data_forwarder', anonymous=True)

    
    global global_pipe_GPS
    global global_pipe_IMU
    global global_pipe_Odomerty 
    global_pipe_GPS = rospy.Publisher('GPS_topic', NavSatFix, queue_size=10)
    global_pipe_IMU = rospy.Publisher('IMU_topic', Imu, queue_size=10)
    global_pipe_Odomerty = rospy.Publisher('Odomerty_topic', Odometry, queue_size=10)


    #cognata
    rospy.Subscriber('/cognataSDK/GPS/imu', Imu, imu_recive, queue_size=1)
    rospy.Subscriber('/cognataSDK/GPS/info', NavSatFix, GPS_recive, queue_size=1)

    # Carla
    rospy.Subscriber("/carla/ego_vehicle/imu", Imu, imu_recive, queue_size=1)
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, GPS_recive, queue_size=1)
    rospy.Subscriber('/carla/ego_vehicle/odometry',Odometry, odometry_recive, queue_size=1) 

    rate = rospy.Rate(10)  # Adjust the publishing rate as needed

    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

	
