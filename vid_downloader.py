import youtube_dl
import os

def download_as_wav(link,location,name):
  path = os.path.join(location,name)
  ydl_opts = {
      'format': 'bestaudio/best',
      'outtmpl':f'{path}',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'wav',
          'preferredquality': '192',
      }],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([link])