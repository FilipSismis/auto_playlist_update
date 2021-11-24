This python script runs through given youtube playlist ids and automatically downloads videos in mp3 format and sorts them to the playlist folders. 
To run the script: 
    -Libraries from requirements.txt need to be installed in your environment
    -Script uses ffmpeg binaries which can be downloaded from: https://www.gyan.dev/ffmpeg/builds/
    -Script running API requests from googles Youtube v3 API api key should be stored in env variable under 'API_KEY'
    -Before starting script specify playlist ids which you want to download in /auo_playlist_update/playlist_ids.txt