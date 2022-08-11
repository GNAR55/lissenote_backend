from huggingsound import SpeechRecognitionModel
from os.path import exists

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")

def stt(audio_paths):

    results = model.transcribe(audio_paths)

    transcriptions = [result['transcription'] for result in results]

    return transcriptions

if __name__=="__main__":
    while True:
        try:
            print(stt(input("Path: ")))
        except:
            pass