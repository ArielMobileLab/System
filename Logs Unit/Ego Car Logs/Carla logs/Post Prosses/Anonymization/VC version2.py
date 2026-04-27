import argparse
import json
import math
import os
import numpy as np
import pedalboard
from pedalboard import (Pedalboard, LowShelfFilter, PeakFilter, HighShelfFilter,
                        Distortion, Compressor)
from pedalboard.io import AudioFile


def pitch_percentage_to_semitones(pct: float) -> float:
    """Convert pitch percentage to semitones. 100% = no change, 78.12% ≈ -4.27 st."""
    if pct <= 0:
        raise ValueError(f"PITCH_PERCENTAGE must be > 0, got {pct}")
    return 12.0 * math.log2(pct / 100.0)


def load_audio(path: str):
    """Load audio file. Returns (channels, samples) float32 array and sample rate."""
    with AudioFile(path) as f:
        audio = f.read(f.frames)
        sr = int(f.samplerate)
    return audio, sr


def save_audio(path: str, audio: np.ndarray, sr: int):
    """Save audio to file. Supports .wav and .mp3."""
    with AudioFile(path, "w", samplerate=sr, num_channels=audio.shape[0]) as f:
        f.write(audio)


def apply_pitch_shift(audio: np.ndarray, sr: int,
                      semitones: float, preserve_formants: bool) -> np.ndarray:
    """Shift pitch without changing duration, with optional formant preservation."""
    if semitones == 0.0:
        return audio
    return pedalboard.time_stretch(
        audio,
        samplerate=sr,
        stretch_factor=1.0,
        pitch_shift_in_semitones=semitones,
        preserve_formants=preserve_formants,
        high_quality=True,
    )


DEFAULTS = {
    "pitch_shifter": {
        "pitch_percentage":  100.0,   # no pitch change
        "preserve_formants": True,
    },
    "equalizer": {
        "low_freq_hz":  100,  "low_gain_db":  0.0,
        "mid_freq_hz":  900,  "mid_gain_db":  0.0,  "mid_q": 1.41,
        "high_freq_hz": 2500, "high_gain_db": 0.0,
    },
    "compressor": {
        "enabled":       False,
        "threshold_db":  -24.0,
        "ratio":         2.0,
        "attack_ms":     10.0,
        "release_ms":    100.0,
    },
    "distortion": {
        "enabled":   False,
        "drive_db":  0.0,
    },
}


def merge(defaults: dict, overrides: dict) -> dict:
    """Return defaults dict with any keys present in overrides applied on top."""
    return {**defaults, **overrides}


def build_fx_chain(eq_cfg: dict, dist_cfg: dict, comp_cfg: dict) -> Pedalboard:
    """Build the full effects chain: EQ → Compressor → Distortion."""
    plugins = []

    # Stage 2: 3-band EQ
    plugins += [
        LowShelfFilter(cutoff_frequency_hz=eq_cfg["low_freq_hz"],  gain_db=eq_cfg["low_gain_db"]),
        PeakFilter(    cutoff_frequency_hz=eq_cfg["mid_freq_hz"],  gain_db=eq_cfg["mid_gain_db"], q=eq_cfg["mid_q"]),
        HighShelfFilter(cutoff_frequency_hz=eq_cfg["high_freq_hz"], gain_db=eq_cfg["high_gain_db"]),
    ]

    # Stage 3: Compressor (optional)
    if comp_cfg.get("enabled", False):
        plugins.append(Compressor(
            threshold_db=comp_cfg["threshold_db"],
            ratio=comp_cfg["ratio"],
            attack_ms=comp_cfg["attack_ms"],
            release_ms=comp_cfg["release_ms"],
        ))

    # Stage 4: Distortion (optional)
    if dist_cfg.get("enabled", False):
        plugins.append(Distortion(drive_db=dist_cfg["drive_db"]))

    return Pedalboard(plugins)


def safe_clip(audio: np.ndarray) -> np.ndarray:
    """Normalize if peak exceeds 1.0 to prevent clipping."""
    peak = np.max(np.abs(audio))
    if peak > 1.0:
        print(f"Clipping guard: normalizing by {peak:.4f}")
        audio = audio / peak
    return audio


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Voice Changer: pitch shift + 3-band EQ + compressor + distortion")
    parser.add_argument("input_file", help="Input audio file (.wav or .mp3)")
    parser.add_argument("config_file", help="JSON config file with processing parameters")
    args = parser.parse_args()

    config = load_config(args.config_file)

    # Output: next to input file, with _output suffix
    base, ext = os.path.splitext(args.input_file)
    output_file = config.get("output_file") or f"{base}_output{ext}"

    pitch_cfg = merge(DEFAULTS["pitch_shifter"], config.get("pitch_shifter", {}))
    eq_cfg    = merge(DEFAULTS["equalizer"],     config.get("equalizer",     {}))
    comp_cfg  = merge(DEFAULTS["compressor"],    config.get("compressor",    {}))
    dist_cfg  = merge(DEFAULTS["distortion"],    config.get("distortion",    {}))

    semitones = pitch_percentage_to_semitones(pitch_cfg["pitch_percentage"])

    print(f"=== Voice Changer ===")
    print(f"Input:  {args.input_file}")
    print(f"Output: {output_file}")
    print(f"Stage 1 — Pitch: {pitch_cfg['pitch_percentage']}% = {semitones:+.4f} semitones | "
          f"Preserve formants: {pitch_cfg['preserve_formants']}")
    print(f"Stage 2 — EQ: {eq_cfg['low_gain_db']:+.1f}dB @ {eq_cfg['low_freq_hz']}Hz | "
          f"{eq_cfg['mid_gain_db']:+.1f}dB @ {eq_cfg['mid_freq_hz']}Hz | "
          f"{eq_cfg['high_gain_db']:+.1f}dB @ {eq_cfg['high_freq_hz']}Hz")
    if comp_cfg.get("enabled"):
        print(f"Stage 3 — Compressor: threshold={comp_cfg['threshold_db']}dB | "
              f"ratio={comp_cfg['ratio']}:1 | attack={comp_cfg['attack_ms']}ms | release={comp_cfg['release_ms']}ms")
    if dist_cfg.get("enabled"):
        print(f"Stage 4 — Distortion: drive={dist_cfg['drive_db']}dB")

    audio, sr = load_audio(args.input_file)
    print(f"Loaded: {audio.shape[1]} samples | {sr} Hz | {audio.shape[0]} channel(s)")

    # Stage 1: pitch shift
    audio = apply_pitch_shift(audio, sr, semitones, pitch_cfg["preserve_formants"])
    print("Stage 1 done.")

    # Stages 2–4: EQ + optional compressor + optional distortion
    fx = build_fx_chain(eq_cfg, dist_cfg, comp_cfg)
    audio = fx(audio, sr)
    print("FX chain done.")

    audio = safe_clip(audio)
    save_audio(output_file, audio, sr)
    print(f"Written: {output_file}")


if __name__ == "__main__":
    print("pedalboard")
    main()