import urllib.request
from image_link_fetcher import *
def download_images(images,file_path='./images/'):
    image_loc = {}
    for key in images:
        full_path = file_path + key + '.jpg'
        image_loc[key] = full_path
        urllib.request.urlretrieve(images[key], full_path)
    return image_loc
#give input as a dictionary with keywords and their respective url's, you get the output dictionary with keywords and their relative location as corresponding values
download_images(get_img_links(["cats","tabletennis","iiit kottayam"]))
