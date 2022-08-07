from urllib.request import urlopen
from wikipedia_links import get_names
import json

def get_img_links(words):
    images={}

    nwords = get_names(words)
    
    for keyword in nwords:
        url = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles="+keyword
        url = url.replace(" ","%20")

        # store the response of URL
        response = urlopen(url)
        # storing the JSON response 
        # from url in data
        data_json = json.loads(response.read())
        page_id = list(data_json['query']['pages'].keys())[0]

        try:
            images[keyword] = data_json['query']['pages'][page_id]['original']['source']
        except:
            pass
            
    return(images)

if __name__=="__main__":
    #input the list, you get a dictionary with the image links. The images are the first image of that wikipedia page
    print(get_img_links(["cats","tabletennis","iiit kottayam"]))

