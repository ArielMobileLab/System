import carla
import math

def main():
    # Connect to client
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)

    # Get World and Actors
    world = client.get_world()
    
    actor_id = None

    # Find the actor ID by type
    actors = world.get_actors()
    for actor in actors:
        if actor.attributes.get('role_name') == 'ego_vehicle':
            ego_vehicle = actor
            actor_id = actor.id
            print(actor_id)
            break

    if actor_id is not None:
	    # Get the vehicle by ID
	    vehicle = world.get_actor(actor_id)
	    physics_control = vehicle.get_physics_control()
	    
	    # Adjust damping rates if needed
	    physics_control.damping_rate_full_throttle = 0.075
	    physics_control.damping_rate_zero_throttle_clutch_engaged = 0.25
	    
	    # Adjust gears and torque curve
	    physics_control.forward_gears = [
		carla.GearPhysicsControl(ratio=2.0, down_ratio=0.5, up_ratio=1.5),
		carla.GearPhysicsControl(ratio=1.9, down_ratio=0.5, up_ratio=1.4),
		carla.GearPhysicsControl(ratio=1.8, down_ratio=0.5, up_ratio=1.3)
		# ... additional gears with similar ratios ...
	    ]
	    physics_control.torque_curve = [
		carla.Vector2D(x=1000.0, y=100.0),
		carla.Vector2D(x=1500.0, y=150.0),
		carla.Vector2D(x=2500.0, y=200.0),
		carla.Vector2D(x=3000.0, y=220.0),
		carla.Vector2D(x=5200.0, y=200.0),
		carla.Vector2D(x=5500.0, y=180.0)
	    ]

            #steering_ratio = 13.9

            #max_steering_wheel_angle_degrees = 450.0
            #Calculate maximum wheel angle in degrees
            #max_wheel_angle_degrees = max_steering_wheel_angle_degrees / steering_ratio
            #Convert angles to radians
            #max_wheel_angle_radians = max_wheel_angle_degrees * (math.pi / 180.0)
	    #print(max_wheel_angle_radians)

 	    #steering_curve = [
            #carla.Vector2D(x=0.0, y=0.0),  # No steering input, no wheel angle
            #carla.Vector2D(x=1.0, y=1.0 / max_wheel_angle_radians)# Full steering input, wheel angle = input / ratio
            #]
	    #physics_control.steering_curve = steering_curve


	    # Apply Vehicle Physics Control for the vehicle
	    vehicle.apply_physics_control(physics_control)

	    print(physics_control)

    else:
        print("No actor of type 'vehicle.nissan.micra' found in the world.")

if __name__ == '__main__':
    main()

