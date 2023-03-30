from pytube import Playlist, YouTube
import time
import os
import urllib.request
import sys

def folderExists(SAVE_PATH, folderName):
    """
    Check whether the downloading folder is present or not. If not then create it
    """
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        print(folderName, " folder is created in Downloads...")
    else:
        print(folderName, " folder already exists....")

def renameingFile(SAVE_PATH, title, index):
    """
    Renaming the downloaded file for serially arrangements of the files.
    """
    print("Renaming...")

    avoid_symbols = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\'', '.', ',']
    for symbol in avoid_symbols:
        for char in title:
            if symbol == char :
                title = title.replace(char, '')            
                
    old_name = SAVE_PATH + r"\{}.mp4".format(title)
    new_name = SAVE_PATH + r"\[ -- {} -- ] {}.mp4".format(str(index), title)
    os.rename(old_name, new_name)
    print("Successfully Rename")
    int(index)

def downloadFile(playlist, from_download, SAVE_PATH):
    """
    Download the file by extracting the playlist and saving it.
    """
    index = 1
    # Count the total number of videos in playlist
    print('Number of videos in playlist: %s' % len(playlist.video_urls))
    print('-'*70)

    # Check whether the playlist url is valid or not
    if len(playlist.video_urls) != 0:
        # Loop through all videos in the playlist and download them
        for url in playlist.video_urls:
            # download from specific video
            if from_download == index:
                start_time = time.perf_counter()     # Start to count the time
                # Check whether the video is available
                try:
                    yt = YouTube(url)
                except VideoUnavailable:
                    print("URL is invalid. Please check the url.")
                else:
                    # Download the video
                    yt.streams.filter(file_extension='mp4', adaptive=True, res='720p')
                    print("Index  : ", index)
                    print('Name  : ', yt.title)
                    print('Link     : ', url)
                    stream = yt.streams.get_by_itag(22)
                    stream.download(SAVE_PATH)

                    stop_time = time.perf_counter()      # Stop to count the time
                    print('Download Successfully....')
                    
                    # Calculating the time to download
                    print(f'Time    : {stop_time - start_time:0.2f} seconds \n')
                    
                    renameingFile(SAVE_PATH, yt.title, index)
                    print('-'*70)
                    from_download+=1
            index+=1
    else:
        print("Youtube Playlist is unavailable")

    # Check whether the all videos are downloaded or not
    if index > 1:
        print("All Videos are downloaded")
        

if __name__ == "__main__":
    playlist = Playlist('https://www.youtube.com/playlist?list=PLbGui_ZYuhigchy8DTw4pX4duTTpvqlh6')
    # start from 1 to length of playlist
    from_download = 1

    try:
        folderName = playlist.title
        SAVE_PATH = os.path.expanduser("~")+"\\Downloads\\" +  folderName
        try:
            folderExists(SAVE_PATH, folderName)
            downloadFile(playlist, from_download, SAVE_PATH)
        except urllib.error.URLError:
            print("Internet is off, please check your connection.")
    except Exception:
        print("URL is Incorrect")
        
    
