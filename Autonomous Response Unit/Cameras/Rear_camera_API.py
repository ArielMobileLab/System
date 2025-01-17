import os
import carla
import numpy as np
import pygame
import subprocess

# Setup the position of the window for the third display
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (3840, 0)

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

# Camera sensor callback
def pygame_callback(data, obj):
    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
    img = img[:, :, :3]
    img = img[:, :, ::-1]  # Convert from RGB to BGR
    img = np.fliplr(img)  # Flip the image horizontally
    obj.surface = pygame.surfarray.make_surface(img.swapaxes(0, 1))

# Setup camera
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '900')
camera_bp.set_attribute('image_size_y', '250')
camera_bp.set_attribute('fov', '100.0')
camera_bp.set_attribute('gamma', '1.8')
camera_bp.set_attribute('iso', '600.0')
camera_bp.set_attribute('shutter_speed', '500.0')

camera_init_trans = carla.Transform(carla.Location(x=-0.5, y=0.0, z=1.63), carla.Rotation(yaw=180))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

# Start camera with PyGame callback
renderObject = RenderObject(900, 250)
camera.listen(lambda image: pygame_callback(image, renderObject))

# Initialize PyGame
pygame.init()
gameDisplay = pygame.display.set_mode((renderObject.surface.get_width(), renderObject.surface.get_height()), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('CARLA Viewer')

# Frame settings
frame_color = (169, 169, 169)  # Black color
frame_thickness = 30  # Increased thickness of the frame

# This function will be called after the window is created to set it always on top
def set_always_on_top():
    pygame.display.flip()  # Ensure the window is created
    window_id = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW']).strip().split()[-1]
    print("Window ID:", window_id)  # Print the window ID for debugging
    subprocess.call(['wmctrl', '-i', '-r', window_id, '-b', 'add,above'])

set_always_on_top()  # Set window always on top

# Game loop
crashed = False
while not crashed:
    world.tick()
    gameDisplay.fill((0, 0, 0))  # Clear the display with a black background
    gameDisplay.blit(renderObject.surface, (0, 0))  # Draw the camera image
    
    # Draw the frame
    pygame.draw.rect(gameDisplay, frame_color, (0, 0, renderObject.surface.get_width(), renderObject.surface.get_height()), frame_thickness)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

camera.stop()
pygame.quit()
