from googleapiclient.discovery import build
from pytube import YouTube
import os


def retrieveVidIds(plId):
    
    api_key = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey = api_key)
    
    request = youtube.playlistItems().list(
            part = 'contentDetails',
            maxResults = '25',
            playlistId = plId
    )

    response = request.execute()

    vidIds = []
    for item in response['items']:
        vidIds.append(item['contentDetails']['videoId'])
    
    return vidIds

def retrievePlaylistName(plId):
    
    api_key = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey = api_key)
    
    request = youtube.playlists().list(
            part = 'snippet',
            id = plId
    )

    response = request.execute()

    for item in response['items']:
        playlistName = item['snippet']['title']
        
    return playlistName


def isUpToDate(retrievedId, playlistName):
    
    lastIdFile = 'last_vid_' + playlistName + '.txt'
    lastId = ''
    
    try:
        with open(lastIdFile) as file:
                lastId = file.read()
    except Exception as e:
        print("Failed to open last_vid")
        
    if(retrievedId == lastId):
        return True
    else:
        return False

        
def downloadMusic(vidIds, playlistName):
    
    url = 'https://www.youtube.com/watch?v='
    lastIdFile = 'last_vid_' + playlistName + '.txt'
    lastId = ''
    
    try:
        with open(lastIdFile) as file:
                lastId = file.read()
    except Exception as e:
        print("Download Music failed with error:" + e)
        
    for vidId in vidIds:
        if not (vidId == lastId):
            downloadSong(url+vidId)
        else:
            break
    
    

def downloadSong(url):
    downloadURL = YouTube(url)
    
    audio = downloadURL.streams.filter(only_audio=True).first()
    audio.download("/Pro/Pyhton Projects/auto_playlist_update/Downloads/")
    
    print("Downloaded succesfully ")
     

def convertMusic(playlistName):
    destination = "D:\\Hudba\\" + playlistName + "\\"
    
    songList = os.listdir(".//Downloads")
    for song in songList:
        convertSong(song, playlistName)
    

def convertSong(songName, playlistName):
    mp4_file = "\"" + ".\\Downloads\\" + songName + "\""
    mp3_file = "\"" + "D:\\Hudba\\" + playlistName + "\\" + songName[:-4] + ".mp3" + "\""
    try:
        cmd = "ffmpeg -i {} -vn {}".format(mp4_file, mp3_file)
        os.system(cmd)
        print("Converted")
    except Exception as e:
        print("Convert Song failed with error:" + e)

def updateLastIdFile(playlistName, lastSongId):
    try:
        lastIdFile = 'last_vid_' + playlistName + '.txt'
        with open(lastIdFile, 'w') as file:
            file.write(lastSongId)
    except Exception as e: 
        print("Update Last Id File failed failed with error:" + e)


def cleanUp():
    songList = os.listdir(".//Downloads")
    for song in songList:
        os.remove(".//Downloads//" + song)
    print("Directory was cleaned up!")


try:
    playlist_ids = open('playlist_ids.txt', 'r')
    for playlistId in playlist_ids:
        plId = playlistId.strip()
        playlistName = retrievePlaylistName(plId)
        vidIds = retrieveVidIds(plId)
        lastSongId = vidIds[0]
        if(isUpToDate(lastSongId, playlistName)):
            print("Playlist: " + playlistName + " is already up to date!")
            continue
        else:
            downloadMusic(vidIds, playlistName)
            convertMusic(playlistName)
            cleanUp()
            updateLastIdFile(playlistName, lastSongId)
            print("Playlist: " + playlistName + " has been updated!")
    playlist_ids.close()
    print("Every playlist is up to date!")        
except Exception as e:
    print("Program failed with error:" + e)

    