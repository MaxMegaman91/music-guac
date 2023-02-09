# The module that does the work
DEBUG = False
from pytube import YouTube
from moviepy.editor import *
import time 
import os
import sys
import getpass

theofficialqual = 0

def info_of_mp3(dictionary_of_info,filenamefull):
    from mutagen.id3 import ID3, TIT2, TPE2, TALB, TPE1, TYER, TDAT, TRCK, TCON, TORY, TPUB, USLT
    audio = ID3(SAVE_PATH+"/"+filenamefull)
    
    audio.add(TIT2(encoding=3, text = dictionary_of_info["TIT2"]))    #TITLE
    audio.add(TPE1(encoding=3, text = dictionary_of_info["TPE1"]))    #ARTIST
    audio.add(TALB(encoding=3, text = dictionary_of_info["TALB"]))    #ALBUM

    audio.save(v2_version=3)

def mp4_to_mp3(mp4, mp3, remove_mp4):
    mp4_without_frames = AudioFileClip(SAVE_PATH+"/"+mp4)
    mp4_without_frames.set_duration(yt.length)
    mp4_without_frames.write_audiofile(SAVE_PATH+"/"+mp3)
    mp4_without_frames.close()
    if remove_mp4: os.remove(SAVE_PATH+"/"+mp4)

def download_by_itag(itag, finalname):
    global yt, SAVE_PATH, name
    try:
        # downloading the video
        yt.streams.get_by_itag(itag).download(output_path=SAVE_PATH, filename=finalname)
    except:
        print("An error occured while trying to download the video/audio!")
        sys.exit("Download error")
        pass

def combine_audio_video(audiofile,videofile,output_file_name_with_extension):
    download_path = "C:/Users/aarus/Downloaded_Youtube"
    videoclip = VideoFileClip(download_path+"/"+videofile)
    audioclip = AudioFileClip(download_path+"/"+audiofile)
    video = videoclip.set_audio(audioclip)
    if theofficialqual == "4k" or theofficialqual == "8k":
        video.write_videofile(str(download_path+"/"+output_file_name_with_extension), fps=60, threads=32)   #macreplace
    else: video.write_videofile(str(download_path+"/"+output_file_name_with_extension), fps=30, threads=32, codec = "libfdk_aac")  #macreplace
    while True: ### check if audio and video files are closed to delete them
        try:
            myfile = open(f'{download_path}/{videofile}', "r+")
            myfile.close()
            os.remove("C:/Users/aarus/Downloaded_Youtube/tempaud.mp4")
            os.remove("C:/Users/aarus/Downloaded_Youtube/tempvid.mp4")
            break                             
        except IOError:
            pass

def findlink(link):
    global yt, name
    # Find video and attach object as variable yt
    print("Finding link: " + link)
    try:
        yt = YouTube(link)
    except:
        print("Not able to find link!")
        sys.exit("LINK NOT FOUND!")
    if name == "":
        name = filenameonly(yt.title)
    info()

def filenameonly(x):
    thelist=[]
    for index in x:
        if index in "abcdefghijklmnopqrstuvwxyz_ ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-":
            thelist.append(index)
    return "".join(thelist).strip()

def checkKey(dict, key):
    if key in dict.keys():
        return True
    else:
        return False

def download_with_qual(qual, finalname):
    global theofficialqual
    theofficialqual = qual
    try:
        if qual != "sd" and qual != "mp3" and qual != "aud" and qual != "usd":
            viditag = yt.streams.filter(res=resolution[qual], mime_type="video/mp4", progressive=False).first().itag
            auditag = yt.streams.filter(mime_type="audio/mp4").get_audio_only().itag
            print("Downloading video!\n")
            download_by_itag(viditag, "tempvid.mp4")
            print("Downloaded video!\n")
            print("Downloading audio!\n")
            download_by_itag(auditag, "tempaud.mp4")
            print("Downloaded audio!\n")
            print("Starting combine!\n")
            combine_audio_video("tempaud.mp4", "tempvid.mp4",finalname+".mp4")
        elif qual == "sd":
            itagofthehighestres = yt.streams.filter(progressive=True).get_highest_resolution().itag
            print("Downloading itag: " + str(itagofthehighestres))
            download_by_itag(itagofthehighestres, finalname+".mp4")
        elif qual == "usd":
            itagofthehighestres = yt.streams.filter(res="360p",progressive=True).get_highest_resolution().itag
            print("Downloading itag: " + str(itagofthehighestres))
            download_by_itag(itagofthehighestres, finalname+".mp4")
        elif qual == "aud" or qual == "mp3":
            auditag = yt.streams.filter(mime_type="audio/mp4").get_audio_only().itag
            print("Downloading itag: " + str(auditag))
            download_by_itag(auditag, "tempaud.mp4")
            mp4_to_mp3("tempaud.mp4", finalname+".mp3", True)    
        print("Product installed and file ready!\n")
    except AttributeError: print("Attribute Error raised: I think you chose a quality not available!")
            

def info():
    enter = "\n"
    print("Video Title: " + yt.title, enter)
    print("Video Author: "+ yt.author, enter)
    print("Video total views: "+ str(yt.views), enter)
    print("Video length: " + str(yt.length//60) + ":" + str(yt.length%60), enter)
    print("Age Restriction: " + str(yt.age_restricted))
    print("press ` for description, else enter to skip")
    if input == "`":
        print("Description Below\n\n\n", yt.description)
    # Print all streams
    for x in yt.streams.filter():
        print(x)

def highestprogrssive():
    # Itag of the highest resolution
    itagofthehighestres = yt.streams.filter(progressive=True).get_highest_resolution().itag
    return (itagofthehighestres)

# Resolutions
resolution = {
    "8k": "4320p",
    "4k": "2160p",
    "uhd": "1440p",
    "hd": "1080p",
    "sd": "720p",
    "mp3": "mp3",
    "aud": "aud",
    "usd": "360p"
}

# The place where videos are downloaded to
SAVE_PATH = "C:/Users/aarus/Downloaded_Youtube"  # macreplace

dictionary_of_info = {
    "TIT2":"",  #TITLE
    "TPE1":"",  #ARTIST
    "TALB":""  #ALBUM
}

# Full loop
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==========================================================================================")
    try: link = input("Give the link of the video needed to be installed: -->  ") # link of the video
    except EOFError: sys.exit("Goodbye! ")
    if link != "txt" and link != "^Z" and len(link.split("|")) < 2:
        name = input("What shall I name the file as? -->  ") #  File name
    else: name = ""
    product = input("Where is this going? --> ")
    if product == "ios": m4v = True
    else: m4v = False
    
    # If we are reading the txt file
    if link == "txt":
        print("==========================================================================================\nReading file!\n\n")
        # Read the text file
        with open("C:/Users/aarus/YT/the.txt", "r") as f:  #macreplace
            mylist = [line.rstrip('\n') for line in f]
        # and read line by line
        lengthoftxt = 0
        for line in mylist:
            findlink(line.split("|")[0]) # Split each line by the | sign, then find the link associated
            download_with_qual(line.split("|")[1], name) # download with the quality on the other side of the |
            needLyrics = False
            if line.split("|")[1] == "mp3": # if its mp3, set name|artist|album
                dictionary_of_info["TIT2"], dictionary_of_info["TPE1"], dictionary_of_info["TALB"]= line.split("|")[2:5]
                if len(line.split("|")) == 6:
                    needLyrics = bool(line.split("|")[6])
                info_of_mp3(dictionary_of_info, name+".mp3")
            if needLyrics:
                from lyrics import getLyrics
                songname, songartist = line.split("|")[2:4]
                getLyrics(songname, songartist)
    elif link == "^Z":sys.exit("Goodbye! ")
    elif len(link.split("|")) >= 2:
        findlink(link.split("|")[0]) # Split each line by the | sign, then find the link associated
        download_with_qual(link.split("|")[1], name) # download with the quality on the other side of the |
        needLyrics = False
        if link.split("|")[1] == "mp3": # if its mp3, set name|artist|album
            dictionary_of_info["TIT2"], dictionary_of_info["TPE1"], dictionary_of_info["TALB"]= link.split("|")[2:5]
            if len(link.split("|")) == 6:
                needLyrics = bool(link.split("|")[6])
            info_of_mp3(dictionary_of_info, name+".mp3")
        if needLyrics:
            from lyrics import getLyrics
            songname, songartist = link.split("|")[2:4]
            getLyrics(songname, songartist)
    # else if we are downloading only one
    elif link[0:3] == "www" or link[0:3] == "htt":
        findlink(link) # Find the link associated yt vid
        itagtouse = input("What quality or itag would you like? -->  ") # Gathering the itag we require
        if itagtouse == "": # Auto download highest progressive source
            itagtouse = highestprogrssive() 
            download_by_itag(itagtouse, name)
        elif checkKey(resolution,itagtouse): # Download with quality input (eg. 4k, hd, uhd, sd, mp3, aud)
            download_with_qual(itagtouse,name)
        elif len(itagtouse.split("&")) == 2: # Download 2 custom itags and combine
            viditag, auditag = itagtouse.split("&")
            print(viditag)
            print(auditag)
            print("Downloading video...")
            download_by_itag(viditag, "tempvid.mp4")
            print("Downloading audio...")
            download_by_itag(auditag, "tempaud.mp4")
            print("Combining...")
            combine_audio_video("tempaud.mp4", "tempvid.mp4",name+".mp4")
            print("Product installed and file ready!\n")
        elif itagtouse[0:5] == "itag:": # specify certain itag
            itagtouse == itagtouse[6:]
            download_by_itag(itagtouse, name)
    
    name = ""
    time.sleep(5)
  