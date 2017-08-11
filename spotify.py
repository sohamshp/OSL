import os
import re
import sys
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib
from mutagen.mp3 import MP3
from mutagen.id3._frames import APIC, TIT2, TALB, TPE1, TRCK, TYER, TCON

### SPOTIFY CLIENT CREDENTIALS
client_id = "c2f4a8f1e315477fb08500b798460812"
client_secret = "546559c5954c411bae9405475fd26dd3"

##MusicXMatch
token = "3f6d99d36b2410b4a22e12de8fa8ca61"

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def customTrim(input_str):
    output_str = re.sub(r'\([^)]*\)', '', input_str)
    output_str = re.sub(r'\{[^}]*\}', '', output_str)
    output_str = re.sub(r'\[[^]]*\]', '', output_str)
    output_str = output_str[:-4].strip()
    print(output_str)
    return output_str


def getFiles(params):
    inputList = os.listdir(params)
    outputList = []
    for data in inputList:
        if ".mp3" in data:
            print(data)
            outputList.append(params + "/" + data)
    return outputList


def loadFile(location):
    audioFile = MP3(location)
    print("Opened file {0}.".format(location))
    return audioFile


def getData(search_param):
    results = spotify.search(search_param)
    displayTrackMenu(results)
    selection = int(input("Enter choice : "))
    return results['tracks']['items'][selection - 1]


def displayTrackMenu(results):
    length = len(results['tracks']['items'])
    if length > 15:
        length = 15
    for iter in range(length):
        print("{0}. {1} - {2}".format(
            str(iter + 1),
            results['tracks']['items'][iter]['name'],
            getAllArtists(results['tracks']['items'][0]['album']['artists'])
        ))


def getAllArtists(artists):
    length = len(artists)
    if length > 3:
        length = 3
    artists_names = [artist['name'] for artist in artists[:length]]
    return ", ".join(artists_names)


def saveAlbumArt(imageUrl):
    urllib.request.urlretrieve(imageUrl, "image.jpg")


def getGenreYear(title, artist):
    url = "http://api.musixmatch.com/ws/1.1/track.search?q_track=" + title + "&q_artist=" + artist + "&page_size=15&apikey=" + token
    url = url.replace(' ', '%20')
    results = requests.get(url).json()
    year = results['message']['body']['track_list'][0]['track']['first_release_date']
    year = year[:4]
    if len(results['message']['body']['track_list'][0]['track']['primary_genres']['music_genre_list'])>=1 :
        genre = results['message']['body']['track_list'][0]['track']['primary_genres']['music_genre_list'][0]['music_genre'][
            'music_genre_name']
    else:
        genre=' '
    return genre, year


def modify(audioFile, trackData):
    artist = getAllArtists(trackData['album']['artists'])
    album = trackData["album"]["name"]
    title = trackData["name"]
    track = str(trackData["track_number"])
    genre, year = getGenreYear(title, artist)
    track.encode('utf-8')
    year.encode('utf-8')

    try:
        audioFile.add_tags()
    except:
        pass

    saveAlbumArt(trackData['album']['images'][0]['url'])

    # Track Title
    audioFile.tags.add(
        TIT2(
            encoding=3,
            text=title
        )
    )
    # Track Album
    audioFile.tags.add(
        TALB(
            encoding=3,
            text=album
        )
    )
    # Track Artist
    audioFile.tags.add(
        TPE1(
            encoding=3,
            text=artist
        )
    )
    # Album Art
    audioFile.tags.add(
        APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc=u"cover",
            data=open('image.jpg', 'rb').read()
        )
    )
    # Track Number
    audioFile.tags.add(
        TRCK(
            encoding=3,
            text=track
        )
    )
    # Track Year
    audioFile.tags.add(
        TYER(
            encoding=3,
            text=year
        )
    )
    # Track Genre
    audioFile.tags.add(
        TCON(
            encoding=3,
            text=genre
        )
    )
    audioFile.update()
    audioFile.tags.update_to_v23()
    audioFile.save(v2_version=3)
    os.remove('image.jpg')


def main():
    for file in getFiles(folder):
        try:
            audioFile = loadFile(file)
            param_str = customTrim(file)
            trackData = getData(param_str.replace(folder + "/", "").replace('_',' '))
            modify(audioFile, trackData)
        except:
            pass
    print('done.')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        folder = "C:\\Users\\Priyank\\Downloads\\Video"
    else:
        folder = sys.argv[1]
    main()
