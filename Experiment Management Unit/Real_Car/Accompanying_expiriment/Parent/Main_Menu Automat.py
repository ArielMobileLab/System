import subprocess
import rospy
import time
from std_msgs.msg import Float64

# Global variables
terminal_opened = False
last_message_time = time.time()  # Track time of the last message
TIMEOUT_DURATION = 10  # Timeout duration in seconds

# Function to start roscore if it's not already running
def start_roscore():
    """Start roscore if it's not already running."""
    try:
        # Check if roscore is running
        subprocess.check_output(["rosnode", "list"])
    except subprocess.CalledProcessError:
        # If not running, start roscore in a new terminal
        print("Starting roscore...")
        subprocess.Popen(["gnome-terminal", "--", "roscore"])
        time.sleep(5)  # Give roscore time to initialize

# Callback function to handle the ROS message and open a terminal when a message is received
def callback(msg):

    global terminal_opened, last_message_time
    
    
    # Update the last message time
    last_message_time = time.time()
    
    # Open the terminal if it hasn't been opened already
    if not terminal_opened:
        print("start")
        command = ["gnome-terminal", "--", "python3", "/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Parent/Automation.py"]
        
        # Run the command to open the terminal
        subprocess.Popen(command)
        
        # Set the terminal_opened flag to True to prevent reopening
        terminal_opened = True

# Function to reset the terminal_opened flag if no message is received within the timeout period
def monitor_inactivity():
    global terminal_opened, last_message_time
    rate = rospy.Rate(1)  # Check every second
    
    while not rospy.is_shutdown():
        # Check if the timeout duration has passed since the last message
        if time.time() - last_message_time > TIMEOUT_DURATION:
            rospy.loginfo("No messages received for a while. Resetting terminal_opened flag.")
            terminal_opened = False  # Reset the terminal_opened flag so terminal can open again
        
        rate.sleep()

# ROS Node initialization
def listener():
    rospy.init_node('scenario_runner', anonymous=True)
    
    # Subscribe to the 'start_scenario' topic
    rospy.Subscriber('/matlab_flag', Float64, callback)
    
    # Monitor inactivity in a separate thread
    monitor_inactivity()

    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    start_roscore()  # Ensure roscore is running
    listener()
