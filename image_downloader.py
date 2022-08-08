import urllib.request
import os

from image_link_fetcher import get_img_links, get_names

def download_images(image_links,file_path='./images/'):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    image_loc = {}

    for key in image_links:
        full_path = file_path + key + '.jpg'
        image_loc[key] = full_path
        urllib.request.urlretrieve(image_links[key], full_path)

    return image_loc

if __name__=="__main__":
    #give input as a dictionary with keywords and their respective url's, you get the output dictionary with keywords and their relative location as corresponding values
    download_images(get_img_links(get_names(["cats","tabletennis","iiit kottayam"])))
