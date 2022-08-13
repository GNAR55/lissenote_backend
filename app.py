from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from flask.json import jsonify
import os

from vid_downloader import download_as_wav
from helper import random_folder, folder_cleanup, audio_to_docx, transcripts_to_pdf
from yt_transcript import video_id, getTranscript

app = Flask("__name__")

temp_path = './temp'

@app.route("/audio", methods=['POST'])
def audio():
    file = request.files['audio']

    if not file:
        print("Invalid file")
        return

    folder_name = random_folder(temp_path)

    filename = secure_filename(file.filename)
    audio_path = os.path.join(folder_name, filename)
    file.save(audio_path)

    pdf_path = audio_to_docx(folder_name, audio_path)

    response = send_from_directory(directory='.', path=pdf_path)

    folder_cleanup(folder_name)

    return response

@app.route("/yt", methods=['POST'])
def yt():
    url = request.form.get("url")

    vid_id = video_id(url)
    if not vid_id:
        print("Invalid URL")
        return jsonify([])

    folder_name = random_folder(temp_path)

    extract_transcription = getTranscript(vid_id)

    if extract_transcription:
        transcript = getTranscript(vid_id)
        pdf_path = transcripts_to_pdf(folder_name, [transcript])
    else:
        audio_path = download_as_wav(url, folder_name)
        pdf_path = audio_to_docx(folder_name, audio_path)

    response = send_from_directory(directory='.', path=pdf_path)

    folder_cleanup(folder_name)

    return response

if __name__ == '__main__':
    app.run(debug=True)