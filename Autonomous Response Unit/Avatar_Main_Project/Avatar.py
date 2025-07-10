import pygame
import threading
import cv2
import numpy as np
import socket
import struct
import logging
import os
import time
from gtts import gTTS

# ======================== UDP CONFIGURATION ========================
IP = "10.20.0.184"
Port = 12355
bufferSize = 2048

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind((IP, Port))

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulation time
simulation_time = 0.0

# ======================== PYGAME SETUP ========================
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avatar מדבר")

WHITE = (255, 255, 255)
font = pygame.font.SysFont("arial", 28)

spoken_text = ""
is_speaking = False
spoken_count = 0
last_time_announcement = 0.0

# ======================== RESOURCE PATHS ========================
BASE_PATH = "/home/auto-tech/Desktop/Avatar project"
video_path = os.path.join(BASE_PATH, "not_move.mp4")
mouth_video_path = os.path.join(BASE_PATH, "move.mp4")

# Load Videos
video_capture = cv2.VideoCapture(video_path)
mouth_video_capture = cv2.VideoCapture(mouth_video_path)

# ======================== FRAME FUNCTIONS ========================
def get_next_video_frame():
    global video_capture
    ret, frame = video_capture.read()
    if not ret or frame is None:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video_capture.read()
        if not ret or frame is None:
            return None
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.flip(frame, 1)
    return frame

def get_next_mouth_frame():
    global mouth_video_capture
    ret, frame = mouth_video_capture.read()
    if not ret or frame is None:
        mouth_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = mouth_video_capture.read()
        if not ret or frame is None:
            return None
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.flip(frame, 1)
    return frame

# ======================== SPEAK FUNCTION ========================
def speak_text(text):
    global is_speaking, spoken_text
    is_speaking = True
    spoken_text = text

    tts = gTTS(text=text, lang='iw')  # Hebrew
    temp_path = "/tmp/voice.mp3"
    tts.save(temp_path)
    os.system(f'mpg123 {temp_path} > /dev/null 2>&1')

    is_speaking = False

# ======================== UDP LISTEN THREAD ========================
def listen_udp():
    global simulation_time
    while True:
        try:
            data, address = UDPClientSocket.recvfrom(bufferSize)
            unpacked_data = struct.unpack("%dd" % (len(data) // 8), data)
            simulation_time = unpacked_data[1]
            logger.info(f"Simulation Time: {simulation_time:.2f}")
        except Exception as e:
            logger.error(f"UDP error: {e}")

# ======================== DRAW FUNCTION ========================
def draw_screen():
    screen.fill(WHITE)

    frame = get_next_video_frame()
    if frame is not None:
        frame = cv2.resize(frame, (500, 500))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
        screen.blit(frame_surface, (0, 0))

    if is_speaking:
        mouth_frame = get_next_mouth_frame()
        if mouth_frame is not None:
            mouth_frame = cv2.resize(mouth_frame, (500, 500))
            mouth_frame = cv2.cvtColor(mouth_frame, cv2.COLOR_BGR2RGB)
            mouth_surface = pygame.image.frombuffer(mouth_frame.tobytes(), mouth_frame.shape[1::-1], "RGB")
            screen.blit(mouth_surface, (0, 0))

    pygame.display.flip()

# ======================== SPEECH SEQUENCE ========================
def speak_twice():
    speak_text("שלום, אני האווטאר שלך.")
    time.sleep(1)

# ======================== PYGAME LOOP ========================
def pygame_loop():
    global spoken_count, last_time_announcement
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_capture.release()
                mouth_video_capture.release()
                pygame.quit()
                exit()
#======================== Conditions that we chose to active the Avatar ======================
        if spoken_count < 1 and simulation_time >= 50:
            threading.Thread(target=speak_twice, daemon=True).start()
            spoken_count += 1
            last_time_announcement = simulation_time
        elif spoken_count >= 1 and simulation_time - last_time_announcement >= 10:
            msg = f"זמן סימולציה {int(simulation_time)} שניות."
            threading.Thread(target=speak_text, args=(msg,), daemon=True).start()
            last_time_announcement = simulation_time

        draw_screen()
        clock.tick(30)

# ======================== START THREADS ========================
threading.Thread(target=listen_udp, daemon=True).start()
threading.Thread(target=pygame_loop, daemon=True).start()

# Keep program running
while True:
    time.sleep(1)
