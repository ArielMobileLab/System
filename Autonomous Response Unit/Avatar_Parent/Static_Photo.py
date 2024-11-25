import rospy
from nav_msgs.msg import Odometry
from PIL import Image, ImageTk
import tkinter as tk

# Global flag to track if the photo has been displayed
photo_displayed = False

def display_photo(photo_path, window_x, window_y, window_width, window_height):
    # Create a Tkinter window
    root = tk.Tk()
    root.geometry("{0}x{1}+{2}+{3}".format(window_width, window_height, window_x, window_y))
    
    # Set the window to be always on top
    root.attributes('-topmost', True)

    # Load the image
    image = Image.open(photo_path)
    
    # Resize the image to fit within the window dimensions
    image.thumbnail((window_width, window_height), Image.ANTIALIAS)
    
    # Convert image to PhotoImage
    photo = ImageTk.PhotoImage(image)

    # Display the image in a label
    label = tk.Label(root, image=photo)
    label.pack(fill=tk.BOTH, expand=True)

    # Keep the window open until closed by the user
    root.mainloop()

def odometry_callback(data):
    global photo_displayed

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

    # Screen dimensions
    single_screen_width = 2150  # Width of a single screen (adjust as necessary)
    screen_height = 1080  # Height of the screens

    # Desired photo window size
    window_width = 250
    window_height = 250

    # Calculate position to center the window at the bottom of the middle screen
    middle_screen_x_start = single_screen_width  # Start of the middle screen
    window_x = middle_screen_x_start + (single_screen_width - window_width) // 2
    window_y = screen_height - window_height - 50  # Adjust to place it slightly above the bottom edge

    # Display photo condition
    if not photo_displayed:
        # Define the path to the photo
        photo_path = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar_video/photo.jpeg'
        display_photo(photo_path, window_x, window_y, window_width, window_height)
        photo_displayed = True

# Initialize ROS node
rospy.init_node('Photo_Agent')

# Subscribe to the odometry topic
rospy.Subscriber("/carla/ego_vehicle/odometry", Odometry, odometry_callback)

# Set the desired loop frequency (1 Hz in this example)
rate = rospy.Rate(1)

# Continue running the code
while not rospy.is_shutdown():
    rate.sleep()
