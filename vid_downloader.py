import youtube_dl
import os

def download_as_mp3(link,location,name="video.mp4"):
    path = os.path.join(location,name)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':f'{path}',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp4',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    
    return path