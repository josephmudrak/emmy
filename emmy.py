import sounddevice as sd
import wavio as wv

from speechbrain.inference.interfaces import foreign_class


def analyse(outfile):
    classifier = foreign_class(
        source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
        pymodule_file="custom_interface.py",
        classname="CustomEncoderWav2vec2Classifier",
    )

    out_prob, score, index, text_lab = classifier.classify_file(outfile)
    return text_lab


def record(frequency, duration, outfile):
    # Start audio recording
    recording = sd.rec(
        int(duration * frequency), samplerate=frequency, channels=2
    )

    # Record audio for given number of seconds
    sd.wait()

    # Convert array to audio file
    wv.write(outfile, recording, frequency, sampwidth=2)
