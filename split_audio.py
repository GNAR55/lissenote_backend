from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_audio(file_path,out_dir,silent_duration=500,thresh=-55):
  sound_file = AudioSegment.from_file(file_path)
  audio_chunks = split_on_silence(sound_file, 
      min_silence_len=silent_duration,
      # consider it silent if quieter than -16 dBFS
      silence_thresh=thresh
  )

  for i, chunk in enumerate(audio_chunks):
      out_file = os.path.join(out_dir,"chunk{0}.wav".format(i))
      print("exporting", out_file)
      chunk.export(out_file, format="wav")