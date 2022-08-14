from transformers import Wav2Vec2ProcessorWithLM
processor = Wav2Vec2ProcessorWithLM.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-english")
processor.save_pretrained("./test")
