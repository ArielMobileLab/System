import sys
import wave
import contextlib
import webrtcvad


def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        sample_rate = wf.getframerate()
        num_frames = wf.getnframes()
        pcm_data = wf.readframes(num_frames)

    if num_channels != 1:
        raise ValueError("WAV must be mono")
    if sample_width != 2:
        raise ValueError("WAV must be 16-bit PCM")
    if sample_rate not in (8000, 16000, 32000, 48000):
        raise ValueError("Sample rate must be 8k/16k/32k/48k")

    return pcm_data, sample_rate


def frame_generator(frame_ms, audio, sample_rate):
    bytes_per_sample = 2
    frame_size = int(sample_rate * (frame_ms / 1000.0) * bytes_per_sample)
    timestamp = 0.0
    duration = frame_ms / 1000.0

    for i in range(0, len(audio) - frame_size + 1, frame_size):
        yield audio[i:i + frame_size], timestamp, duration
        timestamp += duration


def collect_speech_segments(wav_path, out_lab_path, aggressiveness=2, frame_ms=30, min_speech_ms=300, min_silence_ms=300):
    audio, sample_rate = read_wave(wav_path)
    vad = webrtcvad.Vad(aggressiveness)

    frames = list(frame_generator(frame_ms, audio, sample_rate))
    speech_flags = [vad.is_speech(frame, sample_rate) for frame, _, _ in frames]

    segments = []
    start_time = None

    for i, is_speech in enumerate(speech_flags):
        _, timestamp, duration = frames[i]

        if is_speech and start_time is None:
            start_time = timestamp

        elif not is_speech and start_time is not None:
            end_time = timestamp
            if (end_time - start_time) * 1000 >= min_speech_ms:
                segments.append([start_time, end_time])
            start_time = None

    if start_time is not None:
        last_timestamp = frames[-1][1]
        last_duration = frames[-1][2]
        end_time = last_timestamp + last_duration
        if (end_time - start_time) * 1000 >= min_speech_ms:
            segments.append([start_time, end_time])

    merged = []
    for seg in segments:
        if not merged:
            merged.append(seg)
            continue

        prev = merged[-1]
        gap_ms = (seg[0] - prev[1]) * 1000
        if gap_ms <= min_silence_ms:
            prev[1] = seg[1]
        else:
            merged.append(seg)

    with open(out_lab_path, "w", encoding="utf-8") as f:
        for start, end in merged:
            f.write(f"{start:.3f} {end:.3f} sp\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python make_lab.py input.wav output.lab")
        sys.exit(1)

    wav_path = sys.argv[1]
    out_lab_path = sys.argv[2]
    collect_speech_segments(wav_path, out_lab_path)
    print(f"Saved: {out_lab_path}")
