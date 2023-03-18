import shutil
from vimeo_downloader import Vimeo
import moviepy.editor as mp
import speech_recognition as sr
from enum import Enum
import os
import urllib.request
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


class videoType(Enum):
    YOUTUBE = 0
    VIMEO = 1
    OTHER = 2


class audioGrabber:
    __filePath = ""  # where resultant audio should be stored
    __fileName = ""  # name of final audio file
    __url = ""  # url to be downloaded

    def __init__(self, path, file):
        self.__filePath = path
        self.__fileName = file
        os.makedirs(self.__filePath, exist_ok=True)

    def __remExt(self, file):
        return os.path.basename(file).split(".")[0]

    def __youtube(self, url):
        class loggerOutputs:
            def error(msg):
                print("Captured Error: " + msg)

            def warning(msg):
                print("Captured Warning: " + msg)

            def debug(msg):
                print("Captured Log: " + msg)

        fullpath = os.path.join(
            self.__filePath, self.__remExt(self.__fileName) + ".m4a"
        )
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "logger": loggerOutputs,
            "outtmpl": fullpath,
            "postprocessors": [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                }
            ],
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download(url)
            except DownloadError:
                print("An exception has been caught")
                return False

        return True

    def __vimeo(self, url):
        v = Vimeo(url)
        stream = v.streams
        videofile = os.path.splitext(self.__fileName)[0] + ".mp4"
        stream[-1].download(download_directory=self.__filePath, filename=videofile)
        clip = mp.VideoFileClip(os.path.join(self.__filePath, videofile))
        fullpath = os.path.join(self.__filePath, self.__fileName)
        clip.audio.write_audiofile(fullpath)

    def __audlink(self, url):
        file = os.path.join(self.__filePath, self.__fileName)
        print(f"Retrieve {url} to {file}")
        urllib.request.urlretrieve(url, file)

    def dlAudio(self, url):
        self.__url = url
        fullpath = os.path.join(self.__filePath, self.__fileName)
        if not os.path.isfile(fullpath):
            match self.__videotype(self.__url):
                case videoType.YOUTUBE:
                    return self.__youtube(self.__url)
                case videoType.VIMEO:
                    return self.__vimeo(self.__url)
                case videoType.OTHER:
                    return self.__audlink(self.__url)

    def __videotype(self, url):
        url = url.lower()  # remove issues with case sensitivity
        if "youtube" in url or "youtu.be" in url:
            return videoType.YOUTUBE
        elif "vimeo" in url:
            return videoType.VIMEO
        else:
            return videoType.OTHER
