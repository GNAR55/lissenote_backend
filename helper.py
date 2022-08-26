from email.mime import audio
from logging import captureWarnings
import os
import random
import string
import shutil
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask.json import jsonify
from googletrans import Translator

from stt import stt
from keyword_extract import get_keywords_v
from split_audio import split_audio
from wikipedia_links import get_nlinks, get_images
from generate_docx import to_docx
from generate_pdf import to_pdf
from punctuate import punctaute
from yt_transcript import video_id, getTranscript
from vid_downloader import download_as_mp4
from capture_frames import get_frames

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

def transcripts_to_docx(folder_name, transcript_list,translate,language,punctuation=False, frames=[]):
    if punctuation:
        transcript_list = [punctaute(x) for x in transcript_list if x != ' ' and len(x.split()) > 1]
    concat_transcript = ' '.join(transcript_list)

    print(concat_transcript)
    
    keywords = get_keywords_v(concat_transcript)

    if translate==True:
        translator = Translator()
        # image_links = {}
        # image_links = get_images(keywords, file_path=os.path.join(folder_name, 'images/'))
        # captions = list(image_links.keys())
        # print(image_links.values())
        # print(captions)
        # abc = [translator.translate(x,dest=language).text for x in captions]
        # print(abc)
        # image_content = list(zip(list(image_links.values()),[translator.translate(x,dest=language).text for x in captions]))

        image_content = []
    
        # nlinks = get_nlinks(keywords)
        nlinks = []

        docx_path = to_docx(
            translator.translate(keywords[0].title(),dest=language).text, 
            [translator.translate(x,dest=language).text for x in transcript_list], 
            [translator.translate(x,dest=language).text for x in keywords], 
            image_content, 
            nlinks,
            output_directory=folder_name,
            frames=frames)
    else:
        # image_links = get_images(keywords, file_path=os.path.join(folder_name, 'images/'))
        # captions = list(image_links.keys())
        # image_content = list(zip(list(image_links.values()),captions))
        image_content = []

        # nlinks = get_nlinks(keywords)
        nlinks = []

        docx_path = to_docx(
            keywords[0].title(),
            transcript_list, 
            keywords, 
            image_content, 
            nlinks,
            output_directory=folder_name,
            frames=frames)

    return docx_path

def audio_to_docx(folder_name, audio_path,translate,language):
    split_audio_path = os.path.join(folder_name, 'split_files/')
    os.makedirs(split_audio_path)

    split_audio(file_path=audio_path, out_dir=split_audio_path)

    chunk_list = os.listdir(split_audio_path)
    chunk_paths = [os.path.join(split_audio_path, chunk) for chunk in chunk_list]
    chunk_paths.sort()
    transcripts = stt(chunk_paths)

    try:
        frames = get_frames(audio_path, data_path=os.path.join(folder_name, 'data/'), captured_path=os.path.join(folder_name, 'captured/'))
        print("aaaaaaaaaaa")
        print(frames)
    except:
        frames=[]
        print("bbbbbbb")
        print(frames)


    docx_path = transcripts_to_docx(folder_name, transcripts, translate, language, punctuation=True, frames=frames)

    return docx_path



def audio_processing(request, to_pdf=True):
    folder_name = random_folder(temp_path)
    
    file = request.files['audio']
    lang = request.form.get('toLang')

    language=lang

    if lang=='en':
        translate=False
    else:
        translate=True

    if not file:
        print("Invalid file")
        return

    filename = secure_filename(file.filename)
    audio_path = os.path.join(folder_name, filename)
    file.save(audio_path)

    docx_path = audio_to_docx(folder_name, audio_path,translate,language)

    if to_pdf:
        pdf_path = docx_to_pdf(docx_path)
        response = send_from_directory(directory='.', path=pdf_path)
    else:
        response = send_from_directory(directory='.', path=docx_path)
    
    folder_cleanup(folder_name)

    return response

def yt_processing(request, to_pdf=True):
    folder_name = random_folder(temp_path)

    url = request.form.get("url")
    lang = request.form.get('toLang')

    language=lang

    if lang=='en':
        translate=False
    else:
        translate=True

    vid_id = video_id(url)
    if not vid_id:
        print("Invalid URL")
        return jsonify([])

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
        if translate:
            translator = Translator()
            paragraphs = [translator.translate(x,dest=language).text for x in paragraphs]
        docx_path = transcripts_to_docx(folder_name, paragraphs,translate,language)
    else:
        video_path = download_as_mp4(url, folder_name)

        docx_path = audio_to_docx(folder_name, video_path,translate,language)

    if to_pdf:
        pdf_path = docx_to_pdf(docx_path)
        response = send_from_directory(directory='.', path=pdf_path)
    else:
        response = send_from_directory(directory='.', path=docx_path)
    
    # folder_cleanup(folder_name)

    return response