from speechbrain.inference.interfaces import foreign_class


def analyse(outfile):
    classifier = foreign_class(
        source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
        pymodule_file="custom_interface.py",
        classname="CustomEncoderWav2vec2Classifier",
    )

    out_prob, score, index, text_lab = classifier.classify_file(outfile)
    return text_lab
