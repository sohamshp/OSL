import pylast
import eyed3
import os
import sys
import json
import requests
import xml.etree.ElementTree as ET
import spotipy

API_KEY = "8c3232c9ab65219e857b7e9fa38c559f"
API_SECRET = "a6ec7b2d50de468ae805626f67b4a793"
username = "Priyank14"
password_hash = pylast.md5("#1Passwordlast.fm")


def getFiles(params):
    inputList = os.listdir(params)
    outputList = []
    for data in inputList:
        outputList.append(params+"\\"+data)
    return outputList


#def getAlbumArt(function, artist, name):


def loadFile(location):
    audioFile = eyed3.load(location)
    print("Opened file {0} in eyeD3.".format(location))
    return audioFile


def getData(title, artist):
    testa = "linkin park".replace(" ","+")
    testt = "numb".replace(" ","+")
    #param = "https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={0}&artist={1}&track={2}&format=json".format(API_KEY, testa, testt)
    #r = requests.get(param)
    #jsonData = r.json()
    print("hello")
    #return ""


def modify(function, jsonData, name, artist=True, album=True, albumArtist=False):
    artist = jsonData["ArtistName"]
    album = jsonData["AlbumName"]
    print("Modifying tag data of {0} \n".format(name))

    function.tag.artist = artist
    function.tag.album = album
    name = name.replace(artist,'')
    name = name.replace('-','')
    print(name)
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
    for file in getFiles(folder)[1:2]:
        try:
            function = loadFile(file)
            #jsonData = getData(function.tag.title, function.tag.artist)
            spotify = spotipy.Spotify(auth="BQAI6OcBg2NaI36mG63newc7G_AKgVwq7n4lB4esY-OjywGEAlKwXlO1Sv6fxDqj_xEzbS6kTGITuvHeHZrxKF-TT7xqp_zhXQFvJ-f4VbUbaB4zFSvXmsmdV4Aj99PVwrfe7Ztv")
            results = spotify.search("Birds - coldplay")
            ### TITLE
            print(results['tracks']['items'][0]['name'])
            ### ALBUM
            print(results['tracks']['items'][0]['album']['name'])
            ### ARTIST
            print(results['tracks']['items'][0]['album']['artists'][0]['name'])
            ### ALBUM ART URL
            print(results['tracks']['items'][0]['album']['images'][0]['url'])

            '''
            if not jsonData:
                pass
            else:
                status, art = modify(function, jsonData, function.tag.title)
            '''

        except:
            pass

    print("done.")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        folder = "C:\\Users\\shp\\Music\\Music\\Coldpaly - A Head Full of Dreams (2014)" ### some folder name [default]
    else:
        folder = sys.argv[1]

    '''
    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=username,
        password_hash=password_hash
    )
    '''

    print("start.")
    main()
