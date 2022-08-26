import youtube_dl
import os

def download_as_mp4(link,location,name="video.mp4"):
    path = os.path.join(location,name)
    ydl_opts = {
        'format': 'mp4',
        'outtmpl':f'{path}',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    
    return path