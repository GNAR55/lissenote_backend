import os
import random
import string
import shutil

from stt import stt
from keyword_extract import get_keywords_v
from split_audio import split_audio
from wikipedia_links import get_nlinks, get_images
from generate_docx import to_docx
from generate_pdf import to_pdf

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

def transcripts_to_pdf(folder_name, transcript_list):
    concat_transcript = ' '.join(transcript_list)

    print(concat_transcript)

    keywords = get_keywords_v(concat_transcript, num=5)

    image_links = get_images(keywords, file_path=os.path.join(folder_name, 'images/'))

    docx_path = to_docx(keywords[0], transcript_list, keywords, image_links, get_nlinks(keywords), output_directory=folder_name)
    to_pdf(docx_path)

    pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
    return pdf_path

def audio_to_docx(folder_name, audio_path):
    split_audio_path = os.path.join(folder_name, 'split_files/')
    os.makedirs(split_audio_path)

    split_audio(file_path=audio_path, out_dir=split_audio_path)

    chunk_list = os.listdir(split_audio_path)
    chunk_paths = [os.path.join(split_audio_path, chunk) for chunk in chunk_list]
    chunk_paths.sort()
    transcripts = stt(chunk_paths)

    pdf_path = transcripts_to_pdf(folder_name, transcripts)
    return pdf_path
