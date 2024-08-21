import sounddevice as sd
import wavio as wv

from speechbrain.inference.interfaces import foreign_class

# Sampling frequency
freq = 44100

# Recording duration
duration = 5

# Start audio recording
recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

# Record audio for given number of seconds
sd.wait()

# Convert array to audio file
wv.write("recording1.wav", recording, freq, sampwidth=2)

classifier = foreign_class(
    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier",
)
out_prob, score, index, text_lab = classifier.classify_file("recording1.wav")
print(text_lab)
