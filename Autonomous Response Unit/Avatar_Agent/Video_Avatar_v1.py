import rospy
from nav_msgs.msg import Odometry
import cv2
import time
from Xlib import X, display, Xatom

first_video_played = False  # Global flag to track if the video has been played
#second_video_played = False

def odometry_callback(data):
    
    global first_video_played  # Declare the use of the used video flag
    #global second_video_played 


    # First video
    if 141.5689 < data.pose.pose.position.x < 158.4301 and not first_video_played:
        video_path1 = '/home/omer/Desktop/Voice/sample_640x360.mov'
        window_config = {'video1': {'path': video_path1, 'width': 1000, 'height': 1000, 'x': 0, 'y': 0}}
        config = window_config['video1']
        cap = cv2.VideoCapture(config['path'])
        fps = cap.get(cv2.CAP_PROP_FPS)
        wait_time = int(1000 / fps)
        window_width = config['width']
        window_height = config['height']
        window_x = config['x']
        window_y = config['y']

        # Setup the window for video display
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video', window_width, window_height)
        cv2.moveWindow('Video', window_x, window_y)
        time.sleep(0.1)

        # Main loop to play the video
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Reached end of video or failed to read the frame.")
                break

            # Resize the frame to the desired window size
            frame = cv2.resize(frame, (window_width, window_height))
            cv2.imshow('Video', frame)

            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        first_video_played = True  # Set the flag to True after playing the video


    # secound video
    #if 141.5689 < data.pose.pose.position.x < 158.4301 and not second_video_played:
    #     .....
    #     second_video_played = True 



# Initialize ROS node
rospy.init_node('Video_Agent')

# Subscribe to the odometry topic
rospy.Subscriber("/carla/ego_vehicle/odometry", Odometry, odometry_callback)

# Set the desired loop frequency (1 Hz in this example)
rate = rospy.Rate(1)

# Continue running the code
while not rospy.is_shutdown():
    rate.sleep()

