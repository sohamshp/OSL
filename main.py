import eyed3
import os
import sys
import spotipy
import requests

### SPOTIFY
oauthToken = "BQDm11wKhdp4Ozltzx8YrCyaG_ifVPgZrTi7UHunwhDGVJxk9eyf4utDCoV5OciVKex6v_k62Rx_a3fiIWof1AYZRBvWJsvoa9ZdrTu57zEEUtJ8OGF0cXGV0HL3EusXTqzWLbru"

##MusicXMatch
token = "3f6d99d36b2410b4a22e12de8fa8ca61"

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

def musicxmatch(song):
    url = "http://api.musixmatch.com/ws/1.1/track.search?q=" + song + "&page_size=15&apikey=" + token
    url = url.replace(' ','%20')
    results = requests.get(url).json()
    k = 1
    print('select appropriate song')
    for i in results['message']['body']['track_list']:
        print(str(k) + '. ' + i['track']['track_name'] + ' - ' + i['track']['artist_name'])
        k+=1
    choice = int(input()) - 1
    songid = results['message']['body']['track_list'][choice]['track']['track_id']
    #Track Name
    print(results['message']['body']['track_list'][choice]['track']['track_name'])
    #Artist name
    print(results['message']['body']['track_list'][choice]['track']['artist_name'])
    #Album Name
    print(results['message']['body']['track_list'][choice]['track']['album_name'])
    #Genre
    print(results['message']['body']['track_list'][choice]['track']['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name'])





def main():
#    print("Folder: {0}".format(folder))
    musicxmatch('yellow - coldplay')
    for file in getFiles(folder)[1:2]:
        try:
            #function = loadFile(file)
            #jsonData = getData(function.tag.title, function.tag.artist)
            spot = spotipy.Spotify(auth=oauthToken)
            results = spot.search("birds")
            print(results)
            ### TITLE
            print(results['tracks']['items'][2]['name'])
            ### ALBUM
            print(results['tracks']['items'][2]['album']['name'])
            ### ARTIST
            print(results['tracks']['items'][2]['album']['artists'][0]['name'])
            ### ALBUM ART URL
            print(results['tracks']['items'][2]['album']['images'][0]['url'])

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
        folder = "C:\\Users\\Priyank\\Music\\English\\Linkin Park\\Hybrid Theory" ### some folder name [default]
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
