from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Initialize the ElevenLabs client
elevenlabs = ElevenLabs(
    api_key="Need to add key"
)




# Hebrew TTS example
audio = elevenlabs.text_to_speech.convert(
    text="red!!! light!!! STOP!!! ",  
    voice_id="TxGEqnHWrfWFTfGW9XjX",  
    model_id="eleven_monolingual_v1",  
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
    text="red!!! light!!! STOP!!!",  
    voice_id="TxGEqnHWrfWFTfGW9XjX",  
    model_id="eleven_monolingual_v1",  
    output_format="mp3_44100_128",
    voice_settings={
        "stability": 0.3,
        "similarity_boost": 0.7,
        "style": 1.0,
        "use_speaker_boost": True
    }
)

play(audio)


