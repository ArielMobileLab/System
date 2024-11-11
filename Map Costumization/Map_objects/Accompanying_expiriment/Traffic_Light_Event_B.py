import rospy
from nav_msgs.msg import Odometry
import threading
import carla

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()
actors = world.get_actors()

traffic_light_id_1 = 83
traffic_light_id_2 = 63
traffic_light_1 = None
traffic_light_2 = None
ramzor_flag_2 = True
ramzor_flag_1 = True
lock = threading.Lock()

for actor in actors:
    if actor.type_id.startswith("traffic.traffic_light"):
        if actor.id == traffic_light_id_1:
            traffic_light_1 = actor
        elif actor.id == traffic_light_id_2:
            traffic_light_2 = actor

if traffic_light_1 is None:
    rospy.logerr("Traffic light with ID 83 not found")
else:
    rospy.loginfo("Traffic light with ID 83 found")

if traffic_light_2 is None:
    rospy.logerr("Traffic light with ID 63 not found")
else:
    rospy.loginfo("Traffic light with ID 63 found")

def set_traffic_light_state(traffic_light, state, duration=None):
    with lock:
        if traffic_light is not None:
            traffic_light.set_state(state)
            if duration and state == carla.TrafficLightState.Red:
                threading.Timer(duration, lambda: set_traffic_light_state(traffic_light, carla.TrafficLightState.Green)).start()
                rospy.loginfo("Traffic light will be set to green after {} seconds".format(duration))

def ramzor(data):
    global ramzor_flag_1, ramzor_flag_2
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

    if ramzor_flag_1 and 332 < x < 340 and -177 < y < -145:
        with lock:
            traffic_light_1.set_state(carla.TrafficLightState.Yellow)
            rospy.loginfo("Traffic light 1 set to yellow")
            threading.Timer(3, lambda: set_traffic_light_state(traffic_light_1, carla.TrafficLightState.Red, duration=10)).start()
            ramzor_flag_1 = False

    if ramzor_flag_2 and 86 < x < 95 and -239.0 < y < -227.0:
        with lock:
            traffic_light_2.set_state(carla.TrafficLightState.Yellow)
            rospy.loginfo("Traffic light 2 set to yellow")
            threading.Timer(3, lambda: set_traffic_light_state(traffic_light_2, carla.TrafficLightState.Red, duration=10)).start()
            ramzor_flag_2 = False

if __name__ == '__main__':
    rospy.init_node('traffic_light_control')
    rospy.loginfo("ROS node initialized")
    rospy.Subscriber('/carla/ego_vehicle/odometry', Odometry, ramzor, queue_size=1)  
    rospy.loginfo("Subscribed to /carla/ego_vehicle/odometry")
    rospy.spin()
