import json
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask.json import jsonify
import os
import random
import string
import shutil

from stt import stt
from keyword_extract import get_keywords_v
from split_audio import split_audio

app = Flask("__name__")

temp_path = './temp'

@app.route("/keywords", methods=['POST'])
def keywords():
    file = request.files['audio']

    if not file:
        print("Invalid file")
        return

    folder_name = os.path.join(temp_path, ''.join(random.choices(string.ascii_letters + string.digits, k=20)))

    filename = secure_filename(file.filename)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    audio_path = os.path.join(folder_name, filename)
    file.save(audio_path)

    split_audio_path = os.path.join(folder_name, 'split_files/')
    os.makedirs(split_audio_path)

    split_audio(file_path=audio_path, out_dir=split_audio_path)

    chunk_list = os.listdir(split_audio_path)
    chunk_paths = [os.path.join(split_audio_path, chunk) for chunk in chunk_list]
    chunk_paths.sort()
    transcripts = stt(chunk_paths)

    concat_transcript = ' '.join(transcripts)

    print(concat_transcript)

    keywords = get_keywords_v(list(concat_transcript), num=5)

    try:
        shutil.rmtree(folder_name)
    except Exception as e:
        print(f"Failed to delete directory {folder_name}")
        print(e)

    ret = {'keywords': keywords}

    return (jsonify(ret))

    # return(jsonify({}))

if __name__ == '__main__':
    app.run(debug=True)