#!/usr/bin/python3
from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp
import shutil
import sys

def download_and_convert(url, folder, notDownloaded):
    try:
        print("Downloading:", url)
        video = YouTube(url)
        video.streams.filter(only_audio=True).first().download(folder)

        # Convert to mp3
        mp4_path = os.path.join(folder, video.title + ".mp4")
        mp3_path = os.path.join(folder, os.path.splitext(video.title)[0] + '.mp3')
        new_file = mp.AudioFileClip(mp4_path)
        new_file.write_audiofile(mp3_path)
        os.remove(mp4_path)

    except Exception as e:
        notDownloaded.append(url)
        print("Error downloading/processing:", url)
        print(e)

def move_to_usb_drive(src_folder, usb_drive_path):
    for file in os.listdir(src_folder):
        if file.endswith('.mp3'):
            src_path = os.path.join(src_folder, file)
            dst_path = os.path.join(usb_drive_path, file)

            # Check if the file already exists on the USB drive before copying
            if not os.path.exists(dst_path):
                shutil.move(src_path, dst_path)
                print("Transferred:", file)
            else:
                print("Skipped (already exists):", file)

if __name__ == "__main__":
    with open("/tmp/yt_python_version.log", "a") as log_file:
        log_file.write("Running yt.py with Python {}\n".format(sys.version))


    playlistUrl = "https://www.youtube.com/watch?v=s88FNBs3jqc&list=PLeztwve5VWctobZA7sFo2gxVzMSQL6Yc4" #str(input("Playlist URL: "))
    playlist = Playlist(playlistUrl)

    folder = "./download"
    os.makedirs(folder, exist_ok=True)
    notDownloaded = []

    # Step 1: Compare Songs
    usb_drive_path = os.path.join(os.sep, "media", "skyflower", "ibiza", "my-car-go-wroom")
    
    print("Content of /media/skyflower/ibiza/my-car-go-wroom directory:")
    print(os.listdir("/media/skyflower/ibiza/my-car-go-wroom"))
    print("USB drive path:", usb_drive_path)
    print("Is accessible?", os.access(usb_drive_path, os.W_OK))
    
    if os.path.exists(usb_drive_path):
        usb_songs = set(os.listdir(usb_drive_path))
        for url in playlist:
            video = YouTube(url)
            mp3_filename = os.path.splitext(video.title)[0] + '.mp3'
            if mp3_filename not in usb_songs:
                download_and_convert(url, folder, notDownloaded)
        print("Comparison completed.")
    else:
        print("USB flash drive not found. Please make sure it's plugged in.")

    # Step 2: Move MP3 files to the USB flash drive
    if os.path.exists(usb_drive_path):
        move_to_usb_drive(folder, usb_drive_path)
        print("MP3 files have been transferred to the USB flash drive.")
    else:
        print("USB flash drive not found. Please make sure it's plugged in.")
