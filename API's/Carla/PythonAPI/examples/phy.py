import carla

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
        if actor.type_id == 'vehicle.nissan.micra':
            actor_id = actor.id
            print(actor_id)
            print("phy on~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
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

	    # Print the modified physics control for debugging
	    print(physics_control)

	    # Apply Vehicle Physics Control for the vehicle
	    vehicle.apply_physics_control(physics_control)

    else:
        print("No actor of type 'vehicle.nissan.micra' found in the world.")

if __name__ == '__main__':
    main()

