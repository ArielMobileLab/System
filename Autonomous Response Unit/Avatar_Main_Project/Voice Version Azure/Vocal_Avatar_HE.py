
import os
import io
from pydub import AudioSegment
from pydub.playback import play
import azure.cognitiveservices.speech as speechsdk

# Azure credentials
api_key = "Need to add"
region = "Need to add"

# Speech config
speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
speech_config.speech_synthesis_voice_name = 'en-US-GuyNeural'
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)
ssml = """
<speak xmlns="https://www.w3.org/2001/10/synthesis" version="1.0" xml:lang="he-IL">
  <voice name="he-IL-AvriNeural">

    <!-- Cheerful (simulated) -->
    <prosody pitch="+5%" rate="medium" volume="soft">
      שים לב לרמזור שמתקרב
    </prosody>

    <!-- Angry (simulated) -->
    <prosody pitch="0%" rate="fast" volume="loud">
      שים לב לרמזור שמתקרב!
    </prosody>

  </voice>
</speak>
"""

# Synthesize from SSML
result = speech_synthesizer.speak_ssml_async(ssml).get()


