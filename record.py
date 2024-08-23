import sounddevice as sd
import wavio as wv


def record(frequency, duration, outfile):
    # Start audio recording
    recording = sd.rec(
        int(duration * frequency), samplerate=frequency, channels=2
    )

    # Record audio for given number of seconds
    sd.wait()

    # Convert array to audio file
    wv.write(outfile, recording, frequency, sampwidth=2)
