"""
Created on Fri Aug 21 14:16:41 2020

@author: Andrea
"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

link = "https://www.timeout.com/london/music/best-party-songs"

page = requests.get(link)
songsSoup = BeautifulSoup(page.text, 'lxml')
elementsSoup = songsSoup.find_all('h3')

print(len(elementsSoup))
del elementsSoup[-1]
print(len(elementsSoup))

elements = list()
divided = list()

for i in range(0, len(elementsSoup)):
    elements.append(elementsSoup[i].get_text().strip())
    elements[i] = re.sub("^\d{1,3}\.|\‘|\’|\'", '', elements[i])
    elements[i] = elements[i].replace('\xa0', '')
    elements[i] = elements[i].replace('\u2008', '')
    
    for letter in range(0, len(elements[i])):
        if ord(elements[i][letter]) == 8211:
             elements[i] = elements[i].replace(chr(8211), chr(45))
    
    divided.append(elements[i].split(chr(45), maxsplit = 1))
                
    for j in range(0, len(divided[i])):
        divided[i][j] = divided[i][j].strip()
    
    if divided[i][0] == 'Robyn' and divided[i][1] == 'Dancing On My Own':
        divided[i][0], divided[i][1] = divided[i][1], divided[i][0]
        #divided.[i].reverse()
    print(divided[i])

with open('best100-dance-songs.txt', 'w') as best:
    best.write(str(divided))

data = {'song_title': [divided[i][0] for i in range(0, len(divided))],
        'artist': [divided[i][1] for i in range(0, len(divided))]}

df = pd.DataFrame(data, columns = ['song_title', 'artist'])

corrected_titles = {27: "I Bet You Look Good on the Dancefloor", 
                    49: "I Wanna Be Your Lover",
                    52: "I'm Coming Out",
                    54: "What'd I Say"}

for k, v in corrected_titles.items():
    df.at[k, 'song_title'] = v

print(df)

df.to_csv('best100-dance-songs.csv')