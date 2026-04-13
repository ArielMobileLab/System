import wave

WAV_PATH = "example.wav"
RTTM_PATH = "example.rttm"
TARGET_SPK = "10"
OUT_PATH = "speaker_10.wav"

segments = []

with open(RTTM_PATH, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 8:
            continue
        if parts[0] != "SPEAKER":
            continue
        if parts[7] != TARGET_SPK:
            continue

        start = float(parts[3])
        dur = float(parts[4])
        end = start + dur
        segments.append((start, end))

if not segments:
    raise ValueError(f"No segments found for speaker {TARGET_SPK}")

with wave.open(WAV_PATH, "rb") as wf:
    nchannels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    nframes = wf.getnframes()
    audio = wf.readframes(nframes)

bytes_per_frame = nchannels * sampwidth

with wave.open(OUT_PATH, "wb") as out:
    out.setnchannels(nchannels)
    out.setsampwidth(sampwidth)
    out.setframerate(framerate)

    for start, end in segments:
        start_frame = int(start * framerate)
        end_frame = int(end * framerate)
        chunk = audio[start_frame * bytes_per_frame:end_frame * bytes_per_frame]
        out.writeframes(chunk)

print(f"Saved {OUT_PATH}")
print(f"Segments used: {len(segments)}")
