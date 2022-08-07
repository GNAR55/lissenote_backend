from urllib.request import urlopen
import requests
import wikipedia
# import json
import json
# store the URL in url as 
# parameter for urlopen
def get_names(l):
    nicenames=[]
    for i in range(len(l)):
        temp = []
        
        temp=wikipedia.search(l[i])
        if len(temp)!=0:
            #print(temp[0])
            nicenames.append(wikipedia.search(l[i])[0])
        #print(nicenames)
    return(nicenames)

def get_img_links(l):
    images={}
    img_links=[]
    l = get_names(l)
    
    for i in range(len(l)):
        
        keyword = l[i] 
        url_id = (
            'https://en.wikipedia.org/w/api.php'
            '?action=query'
            '&prop=info'
            '&inprop=subjectid'
            '&titles=' + keyword +
            '&format=json')
        url_id= url_id.replace(" ","%20")
        #json_response = requests.get(url).json()
        response = urlopen(url_id)

        # storing the JSON response 
        # from url in data
        data_json = json.loads(response.read())
        url = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles="+keyword
        url = url.replace(" ","%20")
        # store the response of URL
        response = urlopen(url)

        # storing the JSON response 
        # from url in data
        data_json = json.loads(response.read())
        page_id = list(data_json['query']['pages'].keys())[0]
        # print the json response
        #print(data_json['query']['pages'][page_id]['original']['source'])
        try:
            images[keyword] = data_json['query']['pages'][page_id]['original']['source']
        except:
            pass
            
    return(images)
#input the list , you get a dictionary with the image links.The images are the first image of that wikipedia page
print(get_img_links(["cats","tabletennis","iiit kottayam"]))

