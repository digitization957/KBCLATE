"""One-off script: synthesizes a short clock-tick click for the last-10-seconds
countdown cue. No external assets needed."""
import math
import struct
import wave

SAMPLE_RATE = 44100


def main():
    duration = 0.09
    freq = 1800
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 55)  # fast percussive decay
        value = math.sin(2 * math.pi * freq * t) * 0.6
        value += math.sin(2 * math.pi * freq * 2.5 * t) * 0.25
        samples.append(value * env)

    peak = max(1.0, max(abs(v) for v in samples))
    pcm = [max(-1.0, min(1.0, v / peak)) for v in samples]
    frames = b"".join(struct.pack("<h", int(v * 32767)) for v in pcm)

    with wave.open("D:/KBC/app/web/assets/sfx/tick.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(frames)

    print("wrote tick.wav")


if __name__ == "__main__":
    main()
