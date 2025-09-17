import socket, logging, ast, re
import azure.cognitiveservices.speech as speechsdk


IP = "10.20.0.184"
Port = 12357
bufferSize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, Port))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

print(f"Listening for UDP messages on {IP}:{Port}...")

# Finds the first (...) block so we ignore any extra text around it
tuple_re = re.compile(r"\((.*)\)$", re.S)  # greedy to the last ')'

while True:
    try:
        data, address = sock.recvfrom(bufferSize)
        message = data.decode("utf-8", errors="ignore").strip()
        print(f"RAW From {address}: {message}")

        # --- keep only the tuple part ---
        m = tuple_re.search(message)
        tuple_text = "(" + m.group(1) + ")" if m else message  # fall back to whole msg

        # --- parse to Python tuple ---
        parsed = ast.literal_eval(tuple_text)

        if isinstance(parsed, tuple) and len(parsed) == 7:
            voice_name, style, style_degree, pitch, rate, volume, text = parsed


            api_key = "NEED TO ADD"
            region = "NEED TO ADD"

            speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
            speech_config.speech_synthesis_voice_name = 'he-IL-AvriNeural'
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
    

            # Build SSML dynamically
            ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
                xmlns:mstts="http://www.w3.org/2001/mstts"
                xml:lang="en-US">
                <voice name="{voice_name}">
                    <mstts:express-as style="{style}" styledegree="{style_degree}">
                        <prosody pitch="{pitch}" rate="{rate}" volume="{volume}">
                            {text}
                        </prosody>
                    </mstts:express-as>
                </voice>
            </speak>
            """

            speech_synthesizer.speak_ssml_async(ssml).get()



        else:
            log.warning(f"Unexpected payload shape: {parsed!r}")

    except Exception as e:
        log.error(f"UDP error: {e}")
