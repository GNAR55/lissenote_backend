from flask import Flask, request
from flask.json import jsonify

from stt import stt
from keyword_extract import get_keywords_v

app = Flask("__name__")

@app.route("/keywords", methods=['POST'])
def keywords():
    input_json = request.get_json(force=True) 

    path = input_json['path']
    transcript = stt(path)

    keywords = get_keywords_v(list(transcript), num=3)

    return keywords

if __name__ == '__main__':
    app.run(debug=True)