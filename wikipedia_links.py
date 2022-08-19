import wikipedia
import wikipediaapi
import urllib.request
import json
import os

from cairosvg import svg2png

def get_names(word_list):
    """This function takes raw list inputs and searches them using wikipedia api and then stores the first results' of each entry in a list."""

    nicenames = []
    for word in word_list:
        search_res = wikipedia.search(word)
        if search_res:
            nicenames.append(search_res[0])

    return nicenames

def get_links(nword_list):
    """this function takes refined list which comes from the get_names function and gives out a list with the corresponding wikipedia pages urls."""

    wiki = wikipediaapi.Wikipedia('en')

    page_links=[]

    for word in nword_list:
        #appends the page to the list
        page = wiki.page(word)

        if(page.exists()):
            #appends the URL to the page
            page_links.append(page.fullurl)

        #takes care of the edge case i.e if the page does not exist,just points to wikipedia home page
        else:
            print("Page about ",word," does not exist")
            page_links.append("https://www.wikipedia.org/")

    return(page_links)

def get_img_links(words):
    images={}

    nwords = get_names(words)
    
    for keyword in nwords:
        url = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles="+keyword
        url = url.replace(" ","%20")

        # store the response of URL
        try:
            response = urllib.request.urlopen(url)
        except:
            continue
        # storing the JSON response 
        # from url in data
        data_json = json.loads(response.read())
        page_id = list(data_json['query']['pages'].keys())[0]

        try:
            images[keyword] = data_json['query']['pages'][page_id]['original']['source']
        except:
            pass
            
    return(images)

def download_images(image_links,file_path='./images/'):
    """Outputs dictionary with keywords and their relative location as corresponding values"""

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    image_loc = {}

    for key in image_links:
        full_path = file_path + key + os.path.splitext(image_links[key])[1]
        image_loc[key] = full_path
        urllib.request.urlretrieve(image_links[key], full_path)
        name,ext = os.path.splitext(image_loc[key])
        if(ext == '.svg'):
            new_path = full_path[:-3]+'png'
            svg2png(url=image_loc[key],write_to=new_path)
            os.remove(image_loc[key])
            image_loc[key] = new_path
            print(image_loc[key])

    return image_loc

def get_images(words, file_path='./images/'):
    ret = download_images(get_img_links(get_names(words)), file_path=file_path)
    return ret

def get_nlinks(words):
    ret = get_links(get_names(words))
    return ret

if __name__=="__main__":
    print(download_images(get_img_links(get_names(["cats","tabletennis","iiit kottayam"]))))
    print(get_links(get_names(["transistor","inductor","moore"])))
