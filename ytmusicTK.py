from tkinter import *
from mytube import *
from ytmusicapi import YTMusic
import os, requests

yt = YTMusic()


def querySearch(search_query):
    return yt.search(search_query, filter="songs", limit=5)

def artistNames(list1):
    artistlist = []
    for artist in list1:
        artistlist.append(artist["name"])
    return ", ".join(artistlist)

def resulttotext(result):
    return f"""Song: {result['title']}
Artist: {artistNames(result['artists'])}
Album: {result['album']['name']}
Explicit: {result['isExplicit']}
"""

def toDownload(selectedDictionary):
    
    songname = selectedDictionary["title"]

    songartist = artistNames(selectedDictionary['artists'])

    songalbum = selectedDictionary["album"]["name"]

    songlink = "https://www.youtube.com/watch?v="+selectedDictionary["videoId"]

    img_url = selectedDictionary['thumbnails'][-1]['url']
    imgPath = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'temp.png')
    response = requests.get(img_url)
    if response.status_code:
        fp = open(imgPath, 'wb')
        fp.write(response.content)
        fp.close()

    print(songname, songartist, songalbum, songlink, sep="\n")

    audioObject = ytAudio(songlink)
    audioObject.download()
    audioObject.metadata(songname, songartist, songalbum, imgPath, True)

def buildResultPage(search_results):
    for x in range(0, 5):
        tempresult = search_results[x]
        Button(window, text=resulttotext(tempresult), command=lambda: toDownload(search_results[x])).grid(row=rowcount+x, column=0, pady= 5)
    
    return

    selection = int(input("Which number do you want? "))-1

    selectedDictionary = search_results[selection]

    
    
window = Tk("aMusic")
window.geometry("700x700")

Label(window, text="aMusic Downloader", font=("Times New Roman", 18, "bold")).grid(row=0, column=0, padx=10, pady=10)
queryBox = Entry(window, bd=1, name="entry", width=50)
queryBox.grid(row=1, column=0, padx=15, pady=15)
submit = Button(window, text="Search", command=lambda: buildResultPage(querySearch(queryBox.get())), width=40).grid(row=2, column=0, padx=15, pady=10, columnspan=1)
rowcount = 3



window.mainloop()