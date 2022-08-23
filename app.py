from flask import Flask, request
from flask_cors import CORS

from helper import audio_processing, yt_processing

app = Flask("__name__")
CORS(app)

@app.route("/audiotopdf", methods=['POST'])
def audiotopdf():
    '''
    Basic Usage:
    curl -F audio=@new1.wav http://http://127.0.0.1:5000/audiotopdf -o notes.pdf
    '''
    
    return audio_processing(request, to_pdf=True)

@app.route("/audiotodocx", methods=['POST'])
def audiotodocx():
    '''
    Basic Usage:
    curl -F audio=@new1.wav http://http://127.0.0.1:5000/audiotodocx -o notes.docx
    '''
    
    return audio_processing(request, to_pdf=False)

@app.route("/yttopdf", methods=['POST'])
def yttopdf():
    '''
    Basic Usage:
    curl -F url=https://www.youtube.com/watch?v=dQw4w9WgXcQ http://localhost:5000/yttopdf -o notes.pdf
    '''
    
    return yt_processing(request, to_pdf=True)

@app.route("/yttodocx", methods=['POST'])
def yttodocx():
    '''
    Basic Usage:
    curl -F url=https://www.youtube.com/watch?v=dQw4w9WgXcQ http://localhost:5000/yttodocx -o notes.docx
    '''
    
    return yt_processing(request, to_docx=False)

@app.route("/")
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)