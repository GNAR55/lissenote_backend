from flask import Flask, request
from werkzeug.utils import secure_filename
from flask.json import jsonify
import os.path

from stt import stt
from keyword_extract import get_keywords_v

app = Flask("__name__")

temp_path = './temp'

@app.route("/keywords", methods=['POST'])
def keywords():
    file = request.files['audio']

    if file:
            filename = secure_filename(file.filename)

            if not os.path.exists(temp_path):
                os.makedirs(temp_path)

            audio_path = os.path.join(temp_path, filename)
            file.save(audio_path)

    transcript = stt(audio_path)

    keywords = get_keywords_v(list(transcript), num=3)

    ret = {'keywords': keywords}

    return (jsonify(ret))

if __name__ == '__main__':
    app.run(debug=True)