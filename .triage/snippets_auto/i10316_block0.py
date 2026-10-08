"""Demonstrate pylint bug with wave module."""

import wave
import struct

if __name__ == "__main__":
    # Create a 2-second blank WAV file
    with wave.open("blank_audio.wav", "wb") as wav_file:
        # Set parameters for a mono 16-bit 44.1kHz WAV file
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(44100)  # 44.1kHz
        wav_file.setnframes(88200)  # 2 seconds * 44100 Hz
        wav_file.setcomptype("NONE", "not compressed")

        # Create silent frame (0 for 16-bit)
        silent_frame = struct.pack("<h", 0)

        # Write all frames at once
        wav_file.writeframes(silent_frame * 88200)

    print("Successfully created blank_audio.wav")
