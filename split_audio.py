from pydub import AudioSegment
from pydub.silence import split_on_silence
import os.path

def split_audio(file_path,out_dir,silent_duration=1000,thresh=-55):
    sound_file = AudioSegment.from_file(file_path)
    audio_chunks = split_on_silence(sound_file, 
        min_silence_len=silent_duration,
        # consider it silent if quieter than -16 dBFS
        silence_thresh=thresh
    )

    for i, chunk in enumerate(audio_chunks):
        out_file = os.path.join(out_dir,f"chunk{i:03d}.wav")
        print("exporting", out_file)
        chunk.export(out_file, format="wav")