from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime
import sys

artist = sys.argv[1].split("-")[0]
song = sys.argv[1].split("-")[1]

similars = {}
urls = []
opts = Options()
opts.add_argument("start-maximized")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--no-sandbox")
opts.add_argument('disable-infobars')
opts.add_argument("--disable-extensions")
opts.add_argument('--headless')
driver = webdriver.Chrome(options=opts)
driver.get("https://genius.com/{}-{}-lyrics".format("-".join(artist.split()), "-".join(song.split())))

label = driver.find_elements_by_class_name("metadata_unit-label")
info = driver.find_elements_by_class_name("metadata_unit-info")
relevant_info = "Artist, Produced by, Written By, Mixing Engineer".lower().split(', ')

for l, i in zip(label, info):
    soup = bs(i.get_attribute('innerHTML'), 'html.parser')
    if(l.text.lower() in relevant_info):
        urls += [i.attrs['href'] for i in soup.find_all('a')]
urls = list(set(urls))

for url in urls:
    driver.get(url)
    songs = driver.find_elements_by_class_name("mini_card-title")
    artists = driver.find_elements_by_class_name("mini_card-subtitle")
    for i,j in zip(songs, artists):
        if(i.text.lower() != song.lower()):
            similars[j.text.split(', ')[0]] = i.text
driver.close()
sims = pd.DataFrame(similars.values(), similars.keys()).reset_index()
sims.columns = ['Artist', 'Song']
print(sims.to_string(index=False))
