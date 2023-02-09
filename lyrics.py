
def getLyrics(searchquery):
    from lyrics_extractor import SongLyrics
    extract_lyrics = SongLyrics("AIzaSyCAs1m8rklE3vYfyryY25u-gD7JuNhPlKs", "51f3092772c0347b5")
    lyricdict = extract_lyrics.get_lyrics(searchquery)
    print(lyricdict["lyrics"])