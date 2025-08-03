
🗣️ Talking Avatar 

This project simulates a visual character (avatar) that responds to real-time simulation events and speaks in Hebrew using Text-to-Speech technology.
The system displays an animated avatar on screen and plays speech audio generated with gTTS (Google Text-to-Speech), based on data received over from simulation source.
⚙️ Key Features:

    UDP communication to receive simulation time from Carla simulation

    Pygame-based UI for displaying the avatar and video playback.

    Hebrew speech synthesis using gTTS

    Trigger rules based on simulation time (speaking  every 10 seconds).

⚠️ Limitations (Current Version):

    Low-level TTS: The speech is generated using basic gTTS, which lacks expressive emotion or dynamic intonation.
    ▶️ For better voice quality and emotional control, integration with ElevenLabs or Azure Neural TTS is prepared in the main folder of the project but not yet active.

    No lip-sync yet: The mouth animation is not synchronized with the actual phonemes or speech timing. It is currently a simple, time-based approximation.
