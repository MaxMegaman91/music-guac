# Debug mode... requires more integration towards code
DEBUG = False
# Importing all Modules
from pytube import YouTube
from moviepy.editor import *
import os
import sys

class URLError(Exception): pass
class DownloadError(Exception): pass


################################################################################################################



class ytVideo():

    def __init__(self, link):

        self.link = link
        self.object = self.findlink(link)

        if self.object == "Invalid Link!": 
            if DEBUG: print(link, " is not valid link")
            raise URLError("Invalid link! ")

        return


    # locate link and set yt to a class with the link
    def findlink(self, link):

        # Find video and attach object as variable yt
        if DEBUG: print("Finding link: " + link)

        try:
            yt = YouTube(link)
        except:
            return "Invalid Link!"

        self.vidname = self.validFilename(yt.title)
        if DEBUG:
            print("\n\nVid name: ", self.vidname)
            print("Info: ", [x for x in self.info()])
            print("Streams: ", [x for x in self.streams()])
        return yt


    # replace string invalid characters to make a valid filename
    def validFilename(self, filename):

        for letter in filename: 
            if letter not in "abcdefghijklmnopqrstuvwxyz_ ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-":
                filename.replace(letter, "", 1)

        return filename


    # print info to make sure the right link was obtained
    def info(self):

        # yield info
        yield "Video Title: " + self.object.title
        yield "Video Author: "+ self.object.author
        yield "Video total views: "+ str(self.object.views)
        yield "Video length: " + str(self.object.length//60) + ":" + str(self.object.length%60).zfill(2)
        yield "Age Restriction: " + str(self.object.age_restricted)
        # yield "Description: ", self.object.description
        

    def streams(self):

        # Yield all streams / itags
        for x in self.object.streams.filter():
            yield x # must decode all itags and attributes for neater space
        

    def downloadByStream(self, stream, finalname="temp", SAVE_PATH="C:/Users/aarus/Downloaded_Youtube"):
        try:
            # downloading the video
            if DEBUG: print(f"Downloading itag {str(stream.itag)}")
            self.object.streams.get_by_itag(stream.itag).download(output_path=SAVE_PATH, filename=finalname+".mp4")
            if DEBUG: print("Downloaded! ")
        except: raise DownloadError("An error occured while trying to download the video/audio!")

        return SAVE_PATH+"/"+finalname+".mp4"


    # download a file with quality input accessing yt object
    def download(self, quality="sd", finalname="", SAVE_PATH="C:/Users/aarus/Downloaded_Youtube"):

        # Resolution from keyword to pixelcount (if already pixelcount, "except" triggered)
        try: quality = {"8k": "4320p", "4k": "2160p", "uhd": "1440p", "hd": "1080p", "sd": "720p", "usd": "360p"}[quality]
        except KeyError: pass

        # setting filename if no name inputted
        if finalname == "": finalname = self.vidname

        streamToUse = self.object.streams.filter(res=quality, mime_type="video/mp4", progressive=True).first()

        if streamToUse == None: # in the case that a progressive quality couldnt be found, we download separately and merge
            vstreamToUse = self.object.streams.filter(res=quality, mime_type="video/mp4", progressive=False).first()
            astreamToUse = self.object.streams.filter(mime_type="audio/mp4").get_audio_only()

            self.vidpath = self.downloadByStream(vstreamToUse, "tempvid")
            self.audpath = self.downloadByStream(astreamToUse, "tempaud")
            
            if DEBUG: print(vstreamToUse, astreamToUse, sep="\n")

            path = self.AVCombine(SAVE_PATH+"/"+finalname+".mp4")
            self.path = path
            return path
        else: # in the case that a progressive quality is found, we just download that one

            if DEBUG: print(streamToUse)

            path = self.downloadByStream(streamToUse, finalname)
            self.path = path
            return path



    # combines a video and audio file for higher quality video files
    def AVCombine(self, outputfile):
        if DEBUG: print("Combining tempaud and tempvid! ")
        videoclip = VideoFileClip(self.vidpath)
        audioclip = AudioFileClip(self.audpath)

        video = videoclip.set_audio(audioclip)
        video.write_videofile(str(outputfile), fps=60, threads=64)
        if DEBUG: print("Combined, now deleting tempaud and tempvid! ")

        # check if audio and video files are closed to delete them
        while True: 
            try:
                myfile = open(outputfile, "r+")
                myfile.close()
                os.remove(self.vidpath)
                os.remove(self.audpath)
                if DEBUG: print("Cleaned up and done! ")
                break                             
            except IOError:
                if DEBUG: print("Couldn't delete the files! ")
                pass
        
        return outputfile
    


class ytAudio():
    
    def __init__(self, link, asmp=3):

        self.link = link
        self.object = self.findlink(link)
        self.asmp = asmp

        if self.object == "Invalid Link!": raise URLError("Invalid link! ")

        return


    # locate link and set yt to a class with the link
    def findlink(self, link):

        # Find video and attach object as variable yt
        if DEBUG: print("Finding link: " + link)

        try:
            yt = YouTube(link)
        except:
            return "Invalid Link!"

        self.vidname = self.validFilename(yt.title)

        if DEBUG:
            print(self.info())
            print(self.streams())
        return yt


    # replace string invalid characters to make a valid filename
    def validFilename(self, filename):

        for letter in filename: 
            if letter not in "abcdefghijklmnopqrstuvwxyz_ ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-":
                filename = filename.replace(letter, "", 1)

        return filename


    # print info to make sure the right link was obtained
    def info(self):

        # yield info
        yield "Video Title: " + self.object.title
        yield "Video Author: "+ self.object.author
        yield "Video total views: "+ str(self.object.views)
        yield "Video length: " + str(self.object.length//60) + ":" + str(self.object.length%60)
        yield "Age Restriction: " + str(self.object.age_restricted)
        # yield "Description: ", self.object.description
        

    def streams(self):

        # Yield all streams / itags
        for stream in self.object.streams.filter():
            yield stream # must decode all itags and attributes for neater space
        

    def downloadByStream(self, stream, finalname="temp", SAVE_PATH="C:/Users/aarus/Downloaded_Youtube"):

        try:
            # downloading the video
            self.object.streams.get_by_itag(stream.itag).download(output_path=SAVE_PATH, filename=finalname+".mp4")
        except: raise DownloadError("An error occured while trying to download the video/audio!")

        return SAVE_PATH+"/"+finalname+".mp4"


    # download a file with quality input accessing yt object
    def download(self, finalname="", SAVE_PATH="C:/Users/aarus/Downloaded_Youtube"):

        # setting filename if no name inputted
        if finalname == "": finalname = self.vidname

        # getting a certain stream to use
        streamToUse = self.object.streams.filter(mime_type="audio/mp4").get_audio_only()

        if DEBUG: print(streamToUse)

        # download and save path as "path"
        path = self.downloadByStream(streamToUse, finalname)

        # convert to mp3 if requested
        if self.asmp == 3: 
            path = self.toMp3(path, SAVE_PATH+"/"+finalname+".mp3")

        # saving path to class
        self.path = path
        return path

    # Converts mp4 to mp3 when requested final product is mp3 
    def toMp3(self, mp4, mp3):

        mp4file = AudioFileClip(mp4)
        mp4file.set_duration(self.object.length)
        mp4file.write_audiofile(mp3)
        mp4file.close()
        os.remove(mp4)

        return mp3
    
    # edits the mp3 info by title, artist, album, and lyrics API
    def metadata(self, title, artist, album, imagePath, wantlyrics=False, lyrics=""):
        from mutagen.id3 import ID3, TIT2, TALB, TPE1, USLT, APIC
        audio = ID3(self.path)
        
        audio.add(TIT2(encoding=3, text = title))    #TITLE
        audio.add(TPE1(encoding=3, text = artist))    #ARTIST
        audio.add(TALB(encoding=3, text = album))    #ALBUM
        audio.add(APIC(encoding=3, mime="image/png", type=3, desc="Cover", data=open(file=imagePath, mode="rb").read()))


        if wantlyrics:
            lyrics = self.getLyrics(title + " by " + artist)
            audio.add(USLT(encoding=3, text = lyrics))
        audio.save(v2_version=3)

    # lyrics API
    def getLyrics(self, searchquery):
        from lyrics_extractor import SongLyrics
        extract_lyrics = SongLyrics("AIzaSyCAs1m8rklE3vYfyryY25u-gD7JuNhPlKs", "51f3092772c0347b5")
        lyricdict = extract_lyrics.get_lyrics(searchquery)
        return lyricdict["lyrics"]


################################################################################################################

# Main loop
def main(FULLFILL=False):
    '''*** Precaution ***'''
    
    while FULLFILL:
        
        os.system('cls' if os.name == 'nt' else 'clear')

        linkinput = input("What is the YouTube link: ")
        isv = input("Would you like video or audio? ")
        isv = True if isv[0].lower() == "v" else False

        if isv:
            mylink = ytVideo(linkinput)
            mylink.download(input("What quality would you like? "), input("What is the name of the file? "))
            del mylink
        elif not isv:
            mylink = ytAudio(linkinput)
            mylink.download()
            mylink.metadata(input("Song title? -> "), input("Song artist? -> "), input("Song album? -> "), True if input("Want lyrics (y/n)? -> ") == "y" else False)




    

################################################################################################################