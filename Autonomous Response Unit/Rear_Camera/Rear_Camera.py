#!/usr/bin/env python2.7
# image view
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import os

rospy.init_node('opencv', anonymous=True)

bridge = CvBridge()
cv_image = None  # Initialize cv_image to None


def show_image(img):
    cv2.imshow("rear_view", img)
    cv2.waitKey(3)


def image_callback(img_msg):
    rospy.loginfo(img_msg.header)
    global cv_image  # Use the global variable cv_image
    try:
        cv_image = cv2.flip(bridge.imgmsg_to_cv2(img_msg, "passthrough"), 1)
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    if cv_image is not None:  # Check if cv_image is not None before processing it
        show_image(cv_image)
        os.system('wmctrl -r "rear_view" -b add,above')


def open_window():
    cv2.namedWindow("rear_view", cv2.WINDOW_NORMAL)
    screen_width = 7680  # total width of the 4 monitors (assuming all have the same resolution)
    window_width, window_height = 1920, 1080  # dimensions of the window
    x = (screen_width - window_width) * 3 // 4  # x-coordinate of the top-left corner in the center of all four monitors
    y = 0  # y-coordinate of the top-left corner (at the top of the screen)
    cv2.moveWindow("rear_view", x, y)
    cv2.resizeWindow("rear_view", 765, 230)
    cv2.imshow("rear_view", np.zeros((window_height, window_width), dtype='uint8'))
    cv2.setWindowProperty("rear_view", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty("rear_view", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)


open_window()
sub_image = rospy.Subscriber("/carla/ego_vehicle/rgb_front/image", Image, image_callback)
rospy.spin()
