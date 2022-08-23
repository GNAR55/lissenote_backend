import os
import random
import string
import shutil
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask.json import jsonify

from stt import stt
from keyword_extract import get_keywords_v
from split_audio import split_audio
from wikipedia_links import get_nlinks, get_images
from generate_docx import to_docx
from generate_pdf import to_pdf
from punctuate import punctaute
from yt_transcript import video_id, getTranscript
from vid_downloader import download_as_wav

temp_path = './temp'

def random_folder(temp_path):
    folder_name = os.path.join(temp_path, ''.join(random.choices(string.ascii_letters + string.digits, k=20)))

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    return folder_name

def folder_cleanup(folder_name):
    try:
        shutil.rmtree(folder_name)
    except Exception as e:
        print(f"Failed to delete directory {folder_name}")
        print(e)

def docx_to_pdf(docx_path):
    to_pdf(docx_path)

    pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
    return pdf_path

def transcripts_to_docx(folder_name, transcript_list,punctuation=False):
    if punctuation:
        transcript_list = [punctaute(x) for x in transcript_list if x != ' ' and len(x.split()) > 1]
    concat_transcript = ' '.join(transcript_list)

    print(concat_transcript)
    
    keywords = get_keywords_v(concat_transcript)

    image_links = get_images(keywords, file_path=os.path.join(folder_name, 'images/'))
    image_content = list(zip(list(image_links.values()),list(image_links.keys())))
    docx_path = to_docx(keywords[0].title(), transcript_list, keywords, image_content, get_nlinks(keywords), output_directory=folder_name)

    return docx_path

def audio_to_docx(folder_name, audio_path):
    split_audio_path = os.path.join(folder_name, 'split_files/')
    os.makedirs(split_audio_path)

    split_audio(file_path=audio_path, out_dir=split_audio_path)

    chunk_list = os.listdir(split_audio_path)
    chunk_paths = [os.path.join(split_audio_path, chunk) for chunk in chunk_list]
    chunk_paths.sort()
    transcripts = stt(chunk_paths)

    docx_path = transcripts_to_docx(folder_name, transcripts,punctuation=True)

    return docx_path

def audio_processing(request, to_pdf=True):
    file = request.files['audio']

    if not file:
        print("Invalid file")
        return

    folder_name = random_folder(temp_path)

    filename = secure_filename(file.filename)
    audio_path = os.path.join(folder_name, filename)
    file.save(audio_path)

    docx_path = audio_to_docx(folder_name, audio_path)

    if to_pdf:
        pdf_path = docx_to_pdf(docx_path)
        response = send_from_directory(directory='.', path=pdf_path)
    else:
        response = send_from_directory(directory='.', path=docx_path)

    folder_cleanup(folder_name)

    return response

def yt_processing(request, to_pdf=True):
    url = request.form.get("url")

    vid_id = video_id(url)
    if not vid_id:
        print("Invalid URL")
        return jsonify([])

    folder_name = random_folder(temp_path)

    extract_transcription = getTranscript(vid_id)

    if extract_transcription:
        transcript = getTranscript(vid_id)
        split_transcript = transcript.split('.')
        split_transcript = [x.strip() for x in split_transcript]
        paragraphs = []
        para = ''
        for i in range(len(split_transcript)):
            para += split_transcript[i]+'.'
            if (i+1)%5 == 0:
                paragraphs.append(para)
                para = ''
        docx_path = transcripts_to_docx(folder_name, paragraphs)
    else:
        audio_path = download_as_wav(url, folder_name)
        docx_path = audio_to_docx(folder_name, audio_path)

    if to_pdf:
        pdf_path = docx_to_pdf(docx_path)
        response = send_from_directory(directory='.', path=pdf_path)
    else:
        response = send_from_directory(directory='.', path=docx_path)

    folder_cleanup(folder_name)

    return response