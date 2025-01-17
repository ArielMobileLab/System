import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import time
import numpy as np
import math

L = 2.875
Kdd = 4.0
alpha_prev = 0
delta_prev = 0

client = carla.Client('localhost', 2000)
client.set_timeout(200)

world = client.get_world()

actors = world.get_actors()
for actor in actors:
    if actor.type_id.startswith("traffic.traffic_light"):
        traffic_light = actor
        # Change the traffic light state to green (Assuming the state is "Green")
        traffic_light.set_state(carla.TrafficLightState.Green)
        traffic_light.set_green_time(10000)  # Optional: Set the green time duration



bp_lib = world.get_blueprint_library()
vehicle_bp = bp_lib.filter('vehicle.tesla.model3')[0]

transform = carla.Transform()

transform.location.x = -507
transform.location.y = 157.0
transform.location.z = 1.0


#    cone_location = carla.Location(x=-507, y=157.0, z=0.0)
#    cone_transform = carla.Transform(cone_location, carla.Rotation(pitch=0, yaw=0.0, roll=0))


transform.rotation.yaw = 90.0
transform.rotation.pitch = 0
transform.rotation.roll = 0

vehicle = world.spawn_actor(vehicle_bp, transform)

spectator = world.get_spectator()
sp_transform = carla.Transform(transform.location + carla.Location(z=90, x=-65, y=20),
                               carla.Rotation(yaw=0.0, pitch=0.0))
spectator.set_transform(sp_transform)

control = carla.VehicleControl()
control.throttle = 0.55
vehicle.apply_control(control)

map = world.get_map()
waypoints = map.generate_waypoints(2.0)

# Vehicle Current Location
vehicle_loc = vehicle.get_location()
wp = map.get_waypoint(vehicle_loc, project_to_road=True,
                      lane_type=carla.LaneType.Driving)
waypoint_list = []
waypoint_obj_list = []


# Calculate Delta
def calc_steering_angle(alpha, ld):
    delta_prev = 0
    delta = math.atan2(2*L*np.sin(alpha), ld)
    delta = np.fmax(np.fmin(delta, 1.0), -1.0)
    if math.isnan(delta):
        delta = delta_prev
    else:
        delta_prev = delta
    
    return delta

# Get target waypoint index
def get_target_wp_index(veh_location, waypoint_list):
    dxl, dyl = [], []
    for i in range(len(waypoint_list)):
        dx = abs(veh_location.x - waypoint_list[i][0])
        dxl.append(dx)
        dy = abs(veh_location.y - waypoint_list[i][1])
        dyl.append(dy)

    dist = np.hypot(dxl, dyl)
    idx = np.argmin(dist) + 4

    # take closest waypoint, else last wp
    if idx < len(waypoint_list):
        tx = waypoint_list[idx][0]
        ty = waypoint_list[idx][1]
    else:
        tx = waypoint_list[-1][0]
        ty = waypoint_list[-1][1]

    return idx, tx, ty, dist


def get_lookahead_dist(vf, idx, waypoint_list, dist):
    ld = Kdd*vf
    # while ld > dist[idx] and (idx+1) < len(waypoint_list):
    #     idx += 1
    return ld


# Debug Helper
def draw(loc1, loc2=None, type=None):
    if type == "string":
        world.debug.draw_string(loc1, "X",
                            life_time=2000, persistent_lines=True)
    elif type == "line":
        world.debug.draw_line(loc1, loc2, thickness=0.8,
         color=carla.Color(r=0, g=255, b=0),
                        life_time=0.5, persistent_lines=True)
    elif type == "string2":
        world.debug.draw_string(loc1, "X", color=carla.Color(r=0, g=255, b=0),
                            life_time=0.3, persistent_lines=True)

# Generate waypoints
noOfWp = 2000
t = 0
while t < noOfWp:
    wp_next = wp.next(5.0)
    if len(wp_next) > 1:
        wp = wp_next[1]
    else:
        wp = wp_next[0]

    waypoint_obj_list.append(wp)
    waypoint_list.insert(t, (wp.transform.location.x, wp.transform.location.y))
    draw(wp.transform.location, type="string")
    t += 1



# Game Loop
t = 0
throttle_value = 0.55  # Initial throttle value
while t < noOfWp:
    veh_transform = vehicle.get_transform()
    veh_location = vehicle.get_location()
    veh_vel = vehicle.get_velocity()
    vf = np.sqrt(veh_vel.x**2 + veh_vel.y**2)
    vf = np.fmax(np.fmin(vf, 2.5), 0.1)

    min_index, tx, ty, dist = get_target_wp_index(veh_location, waypoint_list)
    ld = get_lookahead_dist(vf, min_index, waypoint_list, dist)

    yaw = np.radians(veh_transform.rotation.yaw)
    alpha = math.atan2(ty-veh_location.y, tx-veh_location.x) - yaw

    if math.isnan(alpha):
        alpha = alpha_prev
    else:
        alpha_prev = alpha

    e = np.sin(alpha)*ld
    
    steer_angle = calc_steering_angle(alpha, ld)
    control.steer = steer_angle
    
    # Adjust throttle every 20 points, 20x0.5 = 10sec
    if t % 40 == 0 and t != 0:  # Start adjusting after the first 20 waypoints
        # Change throttle value between 0.6 and 0.3 every 20 points
        if throttle_value == 0.55:
            throttle_value = 0.50
        else:
            throttle_value = 0.55
            
    control.throttle = throttle_value  # Apply the throttle value
    
    vehicle.apply_control(control)

    #draw(waypoint_obj_list[min_index].transform.location, type="string2")


    time.sleep(0.5)

    t += 1

print("Task Done!")
vehicle.destroy()


