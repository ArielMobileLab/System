import pygame
import threading
import cv2
import numpy as np
import socket
import struct
import logging
import os
import time
import azure.cognitiveservices.speech as speechsdk

# ======================== UDP CONFIGURATION ========================
IP = "10.20.0.184"
Port = 12355
bufferSize = 2048

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind((IP, Port))

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================== GLOBAL VARIABLES ========================
Status = 0.0
last_announced_status = None  # Ensures speech is only triggered on status change
spoken_text = ""
is_speaking = False
spoken_count = 0

# ======================== PYGAME SETUP ========================
pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avatar מדבר")

WHITE = (255, 255, 255)
font = pygame.font.SysFont("arial", 28)

# ======================== RESOURCE PATHS ========================
BASE_PATH = "/home/auto-tech/Desktop/Avatar project"
video_path = os.path.join(BASE_PATH, "not_move.mp4")
mouth_video_path = os.path.join(BASE_PATH, "move.mp4")

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

def speak_text(text,emotion):
    print(text)
    global is_speaking, spoken_text
    is_speaking = True
    spoken_text = text

    api_key = "ADD KEY"
    region = "eastus2"

    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_synthesis_voice_name = 'he-IL-AvriNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    
    
    # #HE version:
    # if emotion in (1,2,3,6):
    #     ssml = f"""
    #     <speak xmlns="https://www.w3.org/2001/10/synthesis" version="1.0" xml:lang="he-IL">
    #     <voice name="he-IL-AvriNeural">
    #         <prosody pitch="+0%" rate="medium" volume="soft">
    #         {text}
    #         </prosody>
    #     </voice>
    #     </speak>
    #     """
    # else:
    #     ssml = f"""
    #     <speak xmlns="https://www.w3.org/2001/10/synthesis" version="1.0" xml:lang="he-IL">
    #     <voice name="he-IL-AvriNeural">
    #         <prosody pitch="+10%" rate="fast" volume="x-loud">
    #         {text}
    #         </prosody>
    #     </voice>
    #     </speak>
    #     """



    #EN version:
    if emotion in (1, 2, 3, 6):  # Calm or positive tones → Cheerful
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
            xmlns:mstts="http://www.w3.org/2001/mstts"
            xml:lang="en-US">
        <voice name="en-US-DavisNeural">
            <mstts:express-as style="cheerful" styledegree="1">
            <prosody pitch="0%" rate="medium" volume="soft">
                {text}
            </prosody>
            </mstts:express-as>
        </voice>
        </speak>
        """
    else:  # More urgent emotion → Terrified
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
            xmlns:mstts="http://www.w3.org/2001/mstts"
            xml:lang="en-US">
        <voice name="en-US-DavisNeural">
            <mstts:express-as style="terrified" styledegree="1">
            <prosody pitch="+0%" rate="medium" volume="loud">
                {text}
            </prosody>
            </mstts:express-as>
        </voice>
        </speak>
        """

    speech_synthesizer.speak_ssml_async(ssml).get()
    is_speaking = False

# ======================== UDP LISTEN THREAD ========================
def listen_udp():
    global Status
    while True:
        try:
            data, _ = UDPClientSocket.recvfrom(bufferSize)
            Status = float(struct.unpack("B", data)[0])
        except Exception as e:
            pass

# ======================== DRAW FUNCTION ========================
def draw_screen():
    screen.fill(WHITE)

    frame = get_next_video_frame()
    if frame is not None:
        frame = cv2.resize(frame, (1000, 1000))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
        screen.blit(frame_surface, (0, 0))

    if is_speaking:
        mouth_frame = get_next_mouth_frame()
        if mouth_frame is not None:
            mouth_frame = cv2.resize(mouth_frame, (1000, 1000))
            mouth_frame = cv2.cvtColor(mouth_frame, cv2.COLOR_BGR2RGB)
            mouth_surface = pygame.image.frombuffer(mouth_frame.tobytes(), mouth_frame.shape[1::-1], "RGB")
            screen.blit(mouth_surface, (0, 0))

    pygame.display.flip()


# ======================== MAIN LOOP ========================
def pygame_loop():
    global spoken_count, last_announced_status
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_capture.release()
                mouth_video_capture.release()
                pygame.quit()
                exit()

        # HE Version
        # status_messages = {
        #     1: "שימו לב אדם שחוצה את הכביש",
        #     2: "מכונית כחולה מלפנים",
        #     3: "שימו לב אדם שחוצה את הכביש",
        #     4: "המכונית מלפנים עצרה!! גם אתה צריך לעצור!!!",
        #     5: "שימו לב לרמזור!!! הוא צהוב!!",
        #     6: " לעקוף את המכונית מלפנים ולשים לב למכוניות בנתיב הנגדי"
        # }

               # EN Version
        status_messages = {
            1: "Pay attention, a pedestrian is crossing the street",
            2: "Blue car ahead",
            3: "Pay attention, a pedestrian is crossing the street",
            4: "The car in front has stopped!!",
            5: "Watch the traffic light!!! It's red!!",
            6: "Overtake the car in front and watch for oncoming traffic"
        }

        if Status != last_announced_status and Status in status_messages:
            last_announced_status = Status
            threading.Thread(target=speak_text, args=(status_messages[Status], Status), daemon=True).start()

                     

        draw_screen()
        clock.tick(30)

# ======================== START THREADS ========================
threading.Thread(target=listen_udp, daemon=True).start()
threading.Thread(target=pygame_loop, daemon=True).start()

# Keep the program alive
while True:
    time.sleep(1)


