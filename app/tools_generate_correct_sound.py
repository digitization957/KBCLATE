"""One-off script: synthesizes a pleasant ascending 3-note chime for the
'correct answer' sound effect (C5-E5-G5 major arpeggio with soft envelope).
No external assets / licensing needed. Run once; output is committed to
web/assets/sfx/correct.wav.
"""
import math
import struct
import wave

SAMPLE_RATE = 44100


def note(freq, duration, volume=0.5):
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    attack = int(n_samples * 0.08)
    release = int(n_samples * 0.35)
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = 1.0
        if i < attack:
            env = i / attack
        elif i > n_samples - release:
            env = (n_samples - i) / release
        # slight harmonic richness
        value = math.sin(2 * math.pi * freq * t)
        value += 0.25 * math.sin(2 * math.pi * freq * 2 * t)
        value += 0.1 * math.sin(2 * math.pi * freq * 3 * t)
        samples.append(value * env * volume)
    return samples


def mix(a, b, offset):
    """Overlay b onto a starting at sample index offset."""
    result = list(a)
    if offset + len(b) > len(result):
        result += [0.0] * (offset + len(b) - len(result))
    for i, v in enumerate(b):
        result[offset + i] += v
    return result


def main():
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5 E5 G5 C6
    step = 0.16
    total_len = int(SAMPLE_RATE * (step * len(notes) + 0.6))
    track = [0.0] * total_len
    for idx, freq in enumerate(notes):
        seg = note(freq, 0.5, volume=0.45)
        offset = int(SAMPLE_RATE * step * idx)
        track = mix(track, seg, offset)

    peak = max(1.0, max(abs(v) for v in track))
    pcm = [max(-1.0, min(1.0, v / peak)) for v in track]
    frames = b"".join(struct.pack("<h", int(v * 32767)) for v in pcm)

    with wave.open("D:/KBC/app/web/assets/sfx/correct.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(frames)

    print("wrote correct.wav")


if __name__ == "__main__":
    main()
