from pytube import Playlist, YouTube
import time
import os
import urllib.request
import sys
# from pytube.cli import on_progress


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
    # for symbol in avoid_symbols:
    #     for char in title:
    #         if symbol == char :
    #             title = title.replace(char, '')
    title = ''.join(char for char in title if char not in avoid_symbols)
                
    old_name = SAVE_PATH + r"\{}.mp4".format(title)
    new_name = SAVE_PATH + r"\[ -- {} -- ] {}.mp4".format(str(index), title)
    os.rename(old_name, new_name)
    print("Successfully Rename")
    int(index)

def downloadFile(playlist, from_download, SAVE_PATH):
    """
    Download the file by extracting the playlist and saving it.
    """
    failed = []
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
                try:
                    # Download the video
                    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True) #, on_progress_callback= on_progress
                    print(f"Index  : {index} \nName  : {yt.title} \nLink     : {url}")
                    #yt.streams.filter(file_extension='mp4', adaptive=True, res='720p')
                    #stream = yt.streams.get_by_itag(22)
                    stream = yt.streams.get_highest_resolution()
                    stream.download(SAVE_PATH)
                except Exception as e :
                    print(f"Download Failed \nReason : ", e)
                    failed_video = [index, yt.title, url]
                    failed.append(failed_video)
                    index+=1
                    from_download+=1
                    print('-'*70)
                    continue
                else:
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
    if len(playlist.video_urls) == index:
        print("All Videos are downloaded")
    return failed
        

if __name__ == "__main__":
    try :
        playlist = Playlist('https://www.youtube.com/playlist?list=PLvZGzNEo-9lEOE7dyQYBbADqzB-aTxV0C')
        # start from 1 to length of playlist
        from_download = 1
        folderName = playlist.title
        SAVE_PATH = os.path.expanduser("~")+"\\Downloads\\" +  folderName
        folderExists(SAVE_PATH, folderName)
        print(downloadFile(playlist, from_download, SAVE_PATH))
    except KeyError:
        print("Playlist URL is Incorrect")
    except urllib.error.URLError:
        print("Internet is off, please check your connection.")
    except Exception as e:
        print("Something wents wrong \n Reason : ", e)

#    try:
#        folderName = playlist.title
#        SAVE_PATH = os.path.expanduser("~")+"\\Downloads\\" +  folderName
#        try:
#            folderExists(SAVE_PATH, folderName)
#            downloadFile(playlist, from_download, SAVE_PATH)
#        except urllib.error.URLError:
#            print("Internet is off, please check your connection.")
#    except Exception:
#        print("URL is Incorrect")
        
    
