import eyed3
import os
import re
import sys
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import shutil

### SPOTIFY CLIENT CREDENTIALS
client_id = "c2f4a8f1e315477fb08500b798460812"
client_secret = "546559c5954c411bae9405475fd26dd3"

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
            outputList.append(params+"/"+data)
    return outputList


def loadFile(location):
    audioFile = eyed3.load(location)
    print("Opened file {0} in eyeD3.".format(location))
    return audioFile


def getData(search_param):
    results = spotify.search(search_param)
    displayTrackMenu(results)
    selection = int(input("Enter choice : "))
    return results['tracks']['items'][selection-1]


def displayTrackMenu(results):
    length = len(results['tracks']['items'])
    if length > 15:
        length = 15
    for iter in range(length):
        print("{0}. {1} - {2}".format(
            str(iter+1),
            results['tracks']['items'][iter]['name'],
            getAllArtists(results['tracks']['items'][0]['album']['artists'])
        ))


def getAllArtists(artists):
    length = len(artists)
    if length > 3:
        length = 3
    artists_names = [artist['name'] for artist in artists[:length]]
    return ", ".join(artists_names)


def getAlbumArt(imageUrl):
    response = requests.get(imageUrl, stream=True)
    return response.raw


def modify(audioFile, trackData, artist=True, album=True, albumArt=False):
    artist = getAllArtists(trackData['album']['artists'])
    album = trackData["album"]["name"]
    title = trackData["name"]
    audioFile.tag.artist = artist
    audioFile.tag.album = album
    audioFile.tag.title = title
    audioFile.tag.setTitle(title)
    #audioFile.tag.save(version=(2,4,0))
    print(title, artist, album)
    art = getAlbumArt(trackData['album']['images'][0]['url'])
    audioFile.tag.images.set(3, art, "image/jpeg")
    audioFile.tag.save(version=(2,4,0))
    '''
    picture = getAlbumArt()
    if picture:
        print("Album Art found.")
        imageData = ### load image here ### urllib2.urlopen(picture).read()
        function.tag.images.set(3, imageData, "image/jpeg", u"you can put a description here")
    else:
        print("Album Art not found")
    '''
    return True, artist


def main():
    print("Folder: {0}".format(folder))
    for file in getFiles(folder):
        try:
            audioFile = loadFile(file)
            param_str = customTrim(file)
            trackData = getData(param_str.replace(folder+"/", ""))
            #print(trackData)
            modify(audioFile, trackData)
        except:
            pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        #folder = "C:\\Users\\shp\\Desktop\\osl_test" ### some folder name [default]
        folder = "/home/ubuntu/workspace/OSL"
    else:
        folder = sys.argv[1]
    main()

'''
### TITLE
print(results['tracks']['items'][0]['name'])
### ALBUM
print(results['tracks']['items'][0]['album']['name'])
### ARTIST
print(results['tracks']['items'][0]['album']['artists'][0]['name'])
### ALBUM ART URL
print(results['tracks']['items'][0]['album']['images'][0]['url'])
'''
