import wave
from typing import cast

with wave.open("dummy.wav", "wb") as handle:
    writer = cast(wave.Wave_write, handle)
    writer.setnchannels(2)
    writer.setsampwidth(2)
    writer.setframerate(44100)
