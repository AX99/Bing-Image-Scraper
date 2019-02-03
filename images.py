from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os

search = input("Search for: ")
params = {"q": search, "pq": search}
r = requests.get("http://www.bing.com/images/search", params=params)

soup = BeautifulSoup(r.text, "html.parser")
links = soup.findAll("a", {"class": "thumb"})

# Use below code to save a copy of the parsed HTML page
f = open("test_results.html", "w+")
f.write(str(soup))
f.close()

# loop through links and extracts href and saves the image file in a directory with part of the href as the title
for item in links:
   try:
       img_obj = requests.get(item.attrs["href"])
       title = item.attrs["href"].split("/")[-1]
       print("Downloading image:  " + str(title))
       print()
       img = Image.open(BytesIO(img_obj.content))

       # Creates a folder for scraped images if there isn't one
       if not os.path.isdir("scraped_images"):
           os.makedirs("scraped_images")

       img.save("./scraped_images/" + title, img.format)
   except:
       print("This image could not be downloaded. Trying next")
       print()