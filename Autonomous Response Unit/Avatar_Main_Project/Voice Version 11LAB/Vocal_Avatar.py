from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Initialize the ElevenLabs client
elevenlabs = ElevenLabs(
    api_key="sk_4e8ef70dd79e8504a48a73f2d8df205e2d38afcbf3b44432"
)




# Hebrew TTS example
audio = elevenlabs.text_to_speech.convert(
    text="red!!! light!!! STOP!!! ",  # Hebrew text
    voice_id="TxGEqnHWrfWFTfGW9XjX",  # Choose a voice that works for you
    model_id="eleven_monolingual_v1",  # Recommended for Hebrew
    output_format="mp3_44100_128",
    voice_settings={
        "stability": 0.3,
        "similarity_boost": 0.7,
        "style": 1.0,
        "use_speaker_boost": True
    }
)

play(audio)

audio = elevenlabs.text_to_speech.convert(
    text="red!!! light!!! STOP!!!",  # Hebrew text
    voice_id="TxGEqnHWrfWFTfGW9XjX",  # Choose a voice that works for you
    model_id="eleven_monolingual_v1",  # Recommended for Hebrew
    output_format="mp3_44100_128",
    voice_settings={
        "stability": 0.3,
        "similarity_boost": 0.7,
        "style": 1.0,
        "use_speaker_boost": True
    }
)

play(audio)


