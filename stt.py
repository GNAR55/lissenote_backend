from speech_model import Model

model = Model(model = "JustAHomosapien/wav2vec2-base-nptel-demo-colab", processor = "jonatasgrosman/wav2vec2-large-xlsr-53-english",LM=True,device="cpu")
def stt(audio_paths):

    transcriptions = model.transcribe(audio_paths)
    return transcriptions

if __name__=="__main__":
    while True:
        try:
            print(stt(input("Path: ")))
        except:
            pass