from mytube import *
from ytmusicapi import YTMusic
import os, requests

yt = YTMusic()


def song_filter(list1):
    returnlist = []
    for x in list1:
        returnlist.append(x["title"] + " by " + artist_get(x) + ", on Album "+x["album"]["name"]+" Explicity: " + str(x["isExplicit"]))
    return returnlist

def artistformat(list1):
    for artist in list1[:-3]:
        string += artist
        string += ", "

def artist_get(selectedDictionary):
    artistlist = []
    for artist in selectedDictionary["artists"]:
        artistlist.append(artist["name"])
    return ", ".join(artistlist)

while True:

    os.system('cls' if os.name == 'nt' else 'clear')

    search_query = input("Query? ")
    search_results = yt.search(search_query, filter="songs", limit=5)
    # print(search_results)

    formattedSongList = song_filter(search_results)
    
    for x in range(0, 8):
        print(str(x+1) + ") " + formattedSongList[x])

    selection = int(input("Which number do you want? "))-1

    selectedDictionary = search_results[selection]

    songname = selectedDictionary["title"]

    songartist = artist_get(selectedDictionary)

    songalbum = selectedDictionary["album"]["name"]

    songlink = "https://www.youtube.com/watch?v="+selectedDictionary["videoId"]

    img_url = selectedDictionary['thumbnails'][-1]['url']
    imgPath = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'cover.png')
    response = requests.get(img_url)
    if response.status_code:
        fp = open(imgPath, 'wb')
        fp.write(response.content)
        fp.close()

    print(songname, songartist, songalbum, songlink, sep="\n")

    # print(selectedDictionary)
    
    
    audioObject = ytAudio(songlink)
    audioObject.download()
    audioObject.metadata(songname, songartist, songalbum, imgPath, True)

"""
EXAMPLE SELECTEDDICTIONARY
{'category': 'Songs', 'resultType': 'song', 'title': 'Face 2 Face', 'album': {'name': 'Face 2 Face', 'id': 'MPREb_bgJpAiwkEsQ'}, 'feedbackTokens': {'add': None, 'remove': None}, 'videoId': 'Wy4MTjQDu98', 'videoType': 'MUSIC_VIDEO_TYPE_ATV', 'duration': '2:05', 'year': None, 'artists': [{'name': 'Juice WRLD', 'id': 'UCbn0GRdgsQtl9hlV-IqxFGg'}], 'duration_seconds': 125, 'isExplicit': False, 'thumbnails': [{'url': 'https://lh3.googleusercontent.com/MEh11doRXY-sOkDZ-kJjLrYGf8wSwYKBg9mmFqFh2uEYBLbJ_2Ulx59qV-7Wq1v7HTVv9iglhBSKYyQV=w60-h60-l90-rj', 'width': 60, 'height': 60}, {'url': 'https://lh3.googleusercontent.com/MEh11doRXY-sOkDZ-kJjLrYGf8wSwYKBg9mmFqFh2uEYBLbJ_2Ulx59qV-7Wq1v7HTVv9iglhBSKYyQV=w120-h120-l90-rj', 'width': 120, 'height': 120}]}
"""