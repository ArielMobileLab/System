import carla
import numpy as np
import pygame

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the world object
world = client.get_world()


vehicles = world.get_actors().filter('vehicle.*')
# Find the ego vehicle
ego_vehicle = None
for vehicle in vehicles:
    if vehicle.attributes.get('role_name') == 'ego_vehicle':
        ego_vehicle = vehicle
        break

# Check if ego vehicle is found
if ego_vehicle is None:
    print("Ego vehicle not found")
    exit()

# Render object to keep and pass the PyGame surface
class RenderObject(object):
    def __init__(self, width, height):
        init_image = np.random.randint(0, 255, (height, width, 3), dtype='uint8')
        self.surface = pygame.surfarray.make_surface(init_image.swapaxes(0, 1))

# Camera sensor callback, reshapes raw data from camera into 2D RGB and applies to PyGame surface
def pygame_callback(data, obj):
    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
    img = img[:, :, :3]
    img = img[:, :, ::-1]
    obj.surface = pygame.surfarray.make_surface(img.swapaxes(0, 1))

# Get the blueprint for the camera sensor and modify the resolution
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '5760')
camera_bp.set_attribute('image_size_y', '1050')
camera_bp.set_attribute('fov', '130.0')
#camera_bp.set_attribute('sensor_tick', '0.175')    # Increase sensor tick to lower frame rate
camera_bp.set_attribute('gamma', '1.8')                  # Set gamma to 1.8
camera_bp.set_attribute('iso', '600.0')                  # Set ISO to 600.0
camera_bp.set_attribute('shutter_speed', '500.0') 


# Initialise the camera floating behind the vehicle
camera_init_trans = carla.Transform(carla.Location(x=0.0, y=0.0, z=1.63), carla.Rotation(yaw=0.0))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

# Start camera with PyGame callback
renderObject = RenderObject(5760, 1050)  # Set the render object size to match the camera resolution
camera.listen(lambda image: pygame_callback(image, renderObject))

# Initialise the PyGame interface
pygame.init()
gameDisplay = pygame.display.set_mode((renderObject.surface.get_width(), renderObject.surface.get_height()),
                                      pygame.HWSURFACE | pygame.DOUBLEBUF)
gameDisplay.fill((0, 0, 0))
gameDisplay.blit(renderObject.surface, (0, 0))
pygame.display.flip()

# Game loop
crashed = False
while not crashed:
    # Advance the simulation time
    world.tick()
    # Update the display
    gameDisplay.blit(renderObject.surface, (0, 0))
    pygame.display.flip()
    # Collect key press events
    for event in pygame.event.get():
        # If the window is closed, break the while loop
        if event.type == pygame.QUIT:
            crashed = True

# Stop camera and quit PyGame after exiting game loop
camera.stop()
pygame.quit()

