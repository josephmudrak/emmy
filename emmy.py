import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from speechbrain.inference.interfaces import foreign_class
from werkzeug.utils import secure_filename


def analyse(outfile):
    print(outfile)
    try:
        classifier = foreign_class(
            source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
            pymodule_file="custom_interface.py",
            classname="CustomEncoderWav2vec2Classifier",
        )

        print(f"Analysing file {outfile}")

        text_lab = classifier.classify_file(outfile)
        print(f"Classification result: {text_lab}")

        if text_lab is None:
            raise ValueError("No result returned in classification")

        return text_lab
    except Exception as e:
        print(f"Error during classification: {e}")
        return None


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def get_message():
    return render_template("index.htm")


@app.route("/analyse", methods=["POST"])
def analyse_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["audio"]

    if file.filename == "":
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join("./", filename)

        file.save(file_path)

        emotion = analyse(str(file_path))[3][0]
        print(emotion)

        return jsonify({"message": emotion}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
