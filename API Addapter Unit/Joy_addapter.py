# code for addapt logitec Xbox & Playstation joystics to ros topic

import rospy
from sensor_msgs.msg import Joy

class JoystickHandler:
    def __init__(self):
        rospy.init_node('joystick_handler')
        self.joystick_type = None
        
        # Create a publisher for the new topic
        self.publisher = rospy.Publisher('/addaptive_joy', Joy, queue_size=10)

        self.subscriber = rospy.Subscriber('/joy', Joy, self.joy_callback)

    def joy_callback(self, msg):
        if self.joystick_type is None:
            self.detect_joystick_type(msg)

        # Prepare a new Joy message to publish
        custom_joy_msg = Joy()
        custom_joy_msg.header = msg.header  # Copy the header for timestamp and frame ID

        # Initialize axes array
        custom_joy_msg.axes = [0.0] * 4  # Adjust based on expected axes count

        # Set the axes based on joystick type		
        if self.joystick_type == 'playstation':

            custom_joy_msg.axes[0] = msg.axes[0]  # Steering
            custom_joy_msg.axes[1] = msg.axes[2]  # Gas
            custom_joy_msg.axes[2] = msg.axes[3]  # Brake
        elif self.joystick_type == 'xbox':

            custom_joy_msg.axes[0] = msg.axes[0]  # Steering
            custom_joy_msg.axes[1] = msg.axes[1]  # Gas
            custom_joy_msg.axes[2] = msg.axes[2]  # Brake
        else:
            rospy.logwarn("Unknown joystick type specified!")
            return  # Exit if the joystick type is unknown

        # Assuming buttons are not being modified, copy them directly
        custom_joy_msg.buttons = msg.buttons

        # Publish the new message
        self.publisher.publish(custom_joy_msg)


    def detect_joystick_type(self, msg):
    # Use button count as a first check
	    button_count = len(msg.buttons)
            print(button_count)
	    if button_count > 18:  # Example threshold; adjust based on actual values
		self.joystick_type = 'playstation'
		print("Playstation_joy")
	
	    elif button_count <= 18:
		self.joystick_type = 'xbox'
		print("Xbox_joy")


if __name__ == '__main__':
    try:
        joystick_handler = JoystickHandler()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

