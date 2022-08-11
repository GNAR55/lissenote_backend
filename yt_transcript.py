from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import TextFormatter
from urllib import parse

def video_id(value):
    '''Returns video id from url.'''
    query = parse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    
    return None                 # if fail

def getTranscript(vid_id, choice=False):
    if choice:
        cc_list = YouTubeTranscriptApi.list_transcripts(vid_id)

        cc_list_c = []

        for cc_i, cc in enumerate(cc_list):
            print(f"{cc_i+1}) {cc.language}")
            cc_list_c.append(cc.language)
            # print(f"Automatic: {cc.is_generated}")
            print()

        cc_inp = int(input("Choice: "))-1
        print()

        for cc in cc_list:
            if cc.language == cc_list_c[cc_inp]:
                cc_data = cc.fetch()
                break
    else:
        cc_data = YouTubeTranscriptApi.get_transcript(vid_id)

    transcript = ""

    for i in cc_data:
        transcript += i['text'].translate({ord('\n'): ' '})
        transcript += " "
    
    # formatter = TextFormatter()
    # formatted = formatter.format_transcript(cc_data)
    # print(formatted)

    return transcript

def getChapters():
    pass

if __name__=="__main__":
    url = input("URL: ")
    print()

    vid_id = video_id(url)

    print(getTranscript(vid_id))
