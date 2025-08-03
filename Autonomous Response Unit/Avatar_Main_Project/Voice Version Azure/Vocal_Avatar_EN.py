
import os
import io
from pydub import AudioSegment
from pydub.playback import play
import azure.cognitiveservices.speech as speechsdk

def play_audio_from_bytes(audio_data, format='wave'):
    audio_data_io = io.BytesIO(audio_data)
    audio_segment = AudioSegment.from_file(audio_data_io, format=format)
    play(audio_segment)

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
<speak xmlns="https://www.w3.org/2001/10/synthesis" 
       xmlns:mstts="https://www.w3.org/2001/mstts" 
       version="1.0" xml:lang="en-US">
  <voice name="en-US-GuyNeural">

    <!-- Cheerful -->
    <mstts:express-as style="cheerful" styledegree="1">
      <prosody pitch="+0%" rate="medium" volume="soft">
        pay attention to the traffic light ahead
      </prosody>
    </mstts:express-as>

    <!-- Angry -->
    <mstts:express-as style="angry" styledegree="2">
      <prosody pitch="+0%" rate="fast" volume="loud">
        pay attention to the traffic light ahead!!!
      </prosody>
    </mstts:express-as>

    <!-- Terrified -->
    <mstts:express-as style="terrified" styledegree="2">
      <prosody pitch="+0%" rate="fast" volume="x-loud">
        pay attention to the traffic light ahead!!!
      </prosody>
    </mstts:express-as>

  </voice>
</speak>
"""

# Synthesize from SSML
result = speech_synthesizer.speak_ssml_async(ssml).get()


