import json
import os

from flask import Flask, g, jsonify, make_response, render_template, request
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

        print(f"{t('analysing_file', g.locale)} {outfile}")

        text_lab = classifier.classify_file(outfile)
        print(f"{t('classification_result', g.locale)} {text_lab}")

        if text_lab is None:
            raise ValueError(t("no_result_returned", g.locale))

        return text_lab
    except Exception as e:
        print(f"{t('error_during_classification', g.locale)} {e}")
        return None


app = Flask(__name__)
CORS(app)


@app.before_request
def detect_locale():
    g.locale = request.cookies.get("locale", "en")


# Load translations
def load_translations():
    translations = {}
    translations_dir = "static/lang"

    for filename in os.listdir(translations_dir):
        if filename.endswith(".json"):
            locale = filename.split(".")[0]

            with open(
                os.path.join(translations_dir, filename), "r", encoding="utf-8"
            ) as file:
                translations[locale] = json.load(file)

    return translations


translations = load_translations()


def t(key, locale="en", placeholders=None):
    global translations

    # Fallback to "en" if locale is missing
    locale_translations = translations.get(locale, translations["en"])
    translation = locale_translations.get(key, key)  # Translation or key

    # Replace placeholders
    if placeholders:
        for placeholder, value in placeholders.items():
            translations = translation.replace(
                f"{{{placeholder}}}", str(value)
            )

    return translation


@app.route("/", methods=["GET", "POST"])
def get_message():
    # Determine locale
    locale = request.cookies.get(
        "locale", "en"
    )  # Default to "en" if not provided

    return render_template("index.htm", locale=locale)


@app.route("/set-locale", methods=["POST"])
def set_locale():
    data = request.json
    locale = data.get("locale", "en")  # Default to "en"

    # Store locale in cookie
    response = jsonify(success=True)
    response.set_cookie("locale", locale, samesite="Strict")
    return response


@app.route("/analyse", methods=["POST"])
def analyse_audio():
    if "audio" not in request.files:
        return jsonify({"error": t("no_result_returned", g.locale)}), 400

    file = request.files["audio"]

    if file.filename == "":
        return jsonify({"error": t("no_result_returned", g.locale)}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join("./", filename)

        file.save(file_path)

        emotion = analyse(str(file_path))[3][0]
        print(emotion)

        return jsonify({"message": emotion}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
