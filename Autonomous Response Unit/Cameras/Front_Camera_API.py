import carla
import numpy as np
import pygame

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the world object
world = client.get_world()
# settings = world.get_settings()
# settings.synchronous_mode = True
# settings.fixed_delta_seconds = 1.0 / 20.0  # 1/20 second time step
# world.apply_settings(settings)

# Find the ego vehicle
ego_vehicle = None
for vehicle in world.get_actors().filter('vehicle.*'):
    if vehicle.attributes.get('role_name') == 'ego_vehicle':
        ego_vehicle = vehicle
        break

# Check if ego vehicle is found
if ego_vehicle is None:
    print("Ego vehicle not found")
    exit()

# Total resolution of the three displays
total_display_width = 5760
total_display_height = 1080

# Render object to keep and pass the PyGame surface
class RenderObject(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))

# Camera sensor callback, reshapes raw data from camera into 2D RGB and applies to PyGame surface
def pygame_callback(data, obj):
    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
    img = img[:, :, :3]  # Keep only RGB channels
    img = img[:, :, ::-1]  # Convert BGR to RGB
    obj.surface = pygame.surfarray.make_surface(img.swapaxes(0, 1))

# Get the blueprint for the camera sensor and modify the resolution
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '3500')  # Adjust resolution based on aspect ratio
camera_bp.set_attribute('image_size_y', '1080')
camera_bp.set_attribute('fov', '130.0')
camera_bp.set_attribute('gamma', '1.7')                  # Set gamma to 1.8
camera_bp.set_attribute('iso', '600.0')                  # Set ISO to 600.0
camera_bp.set_attribute('shutter_speed', '500.0')

# Initialise the camera floating behind the vehicle
camera_init_trans = carla.Transform(carla.Location(x=0.12, y=0.0, z=1.60), carla.Rotation(pitch=0.0))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

# Start camera with PyGame callback
renderObject = RenderObject(3500, 1080)  # Set the render object size to match the camera resolution
camera.listen(lambda image: pygame_callback(image, renderObject))


# Initialise the PyGame interface
pygame.init()

# Decide which displays to use (example: using displays 2, 3, and 4)
display_offsets = [1]  # Start positions for each display

# Create the full surface
gameDisplay = pygame.display.set_mode((total_display_width, total_display_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('CARLA Camera Feed')

# Game loop
crashed = False
clock = pygame.time.Clock()
while not crashed:
    # Advance the simulation time
    #world.tick()

    # Scale the camera image to fit across the selected displays
    scaled_img = pygame.transform.scale(renderObject.surface, (total_display_width, total_display_height))
    
    # Clear the game display
    gameDisplay.fill((0, 0, 0))
    
    # Blit the scaled image onto the selected displays
    for offset in display_offsets:
        gameDisplay.blit(scaled_img, (offset, 0))

    # Update the display
    pygame.display.flip()

    # Collect key press events
    for event in pygame.event.get():
        # If the window is closed, break the while loop
        if event.type == pygame.QUIT:
            crashed = True

# Stop camera and quit PyGame after exiting game loop
camera.stop()
pygame.quit()
