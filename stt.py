from huggingsound import SpeechRecognitionModel
from os.path import exists

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")

def stt(audio_path):

    if not exists(audio_path):
        print("File doesn't exist")
        return

    audio_paths = [audio_path]

    transcriptions = model.transcribe(audio_paths)

    transcription = transcriptions[0]['transcription']

    return transcription

if __name__=="__main__":
    while True:
        try:
            print(stt(input("Path: ")))
        except:
            pass