"""One-off script: synthesizes a soft two-note chime played when options are revealed."""
import math
import struct
import wave

SR = 44100


def note(freq, start, dur, out):
    for i in range(int(SR * dur)):
        t = i / SR
        env = min(t / 0.02, 1.0) * math.exp(-t * 6)  # gentle attack, slow decay
        v = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * freq * 2 * t)) * env * 0.35
        idx = int(start * SR) + i
        if idx < len(out):
            out[idx] += v


def main():
    out = [0.0] * int(SR * 1.0)
    note(659.25, 0.0, 0.9, out)   # E5
    note(987.77, 0.12, 0.85, out)  # B5
    frames = b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32767)) for v in out)
    with wave.open("D:/KBC/app/web/assets/sfx/reveal.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(frames)


if __name__ == "__main__":
    main()
