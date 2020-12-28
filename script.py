from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os


def start_search():
    search = input("Search for: ")
    params = {"q": search, "pq": search}
    dir_name = search.replace(" ", "_").lower()

    # Creates a folder for scraped images if there isn't one. The title of the directory is the search term
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    r = requests.get("http://www.bing.com/images/search", params=params)

    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.findAll("a", {"class": "thumb"})

    # Use below code to save a copy of the parsed HTML page
    f = open("test_results.html", "w+")
    f.write(str(soup))
    f.close()

    # Loop through links and extracts href and saves the image file in the search directory
    for item in links:
        img_obj = requests.get(item.attrs["href"])
        title = item.attrs["href"].split("/")[-1]
        print("Title is " + str(title))
        print()
        try:
            img = Image.open(BytesIO(img_obj.content))
            img.save("./" + dir_name + "/" + title, img.format)
        except:
            print("This image could not be downloaded. Trying next")
            print()

    
if __name__ == '__main__':
    start_search()
