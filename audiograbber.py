import shutil
from vimeo_downloader import Vimeo
import moviepy.editor as mp
import speech_recognition as sr
from enum import Enum
import os
import urllib.request
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from audiograbber.stpaul import StPaulVideo
from audiograbber.mankato import Mankato


class videoType(Enum):
    YOUTUBE = 0
    VIMEO = 1
    STPAUL = 2
    MANKATO = 3
    OTHER = 4


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
        print(f"Downloading: {url}")
        class loggerOutputs:
            @staticmethod
            def error(msg):
                print("Captured Error: " + msg)
                
            @staticmethod
            def warning(msg):
                print("Captured Warning: " + msg)

            @staticmethod
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
                    "preferredcodec": "mp3",
                }
            ],
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.cache.remove()
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

    def __stPaul(self, url):
        file = os.path.join(self.__filePath, self.__fileName)
        print(f"Retrieve {url} to {file}")
        spvid = StPaulVideo(url, file)
        spvid.download_mp4()
    
    def __mankato(self, url):
        file = os.path.join(self.__filePath, self.__fileName)
        print(f"Retrieve {url} to {file}")
        mvid = Mankato(url, file)
        mvid.download()


    def dlAudio(self, url):
        self.__url = url
        fullpath = os.path.join(self.__filePath, self.__fileName)
        if not os.path.isfile(fullpath):
            match self.__videotype(self.__url):
                case videoType.YOUTUBE:
                    return self.__youtube(self.__url)
                case videoType.VIMEO:
                    #return self.__vimeo(self.__url)
                    res = self.__youtube(self.__url)
                    if not res:
                        return self.__vimeo(self.__url)
                    else:
                        return res
                case videoType.STPAUL:
                    return self.__stPaul(self.__url)
                case videoType.MANKATO:
                    return self.__mankato(self.__url)
                case videoType.OTHER:
                    return self.__audlink(self.__url)

    def __videotype(self, url):
        url = url.lower()  # remove issues with case sensitivity
        if "youtube" in url or "youtu.be" in url:
            return videoType.YOUTUBE
        elif "vimeo" in url:
            return videoType.VIMEO
        elif "eduvision" in url:
            return videoType.STPAUL
        elif "mankatoaps" in url:
            return videoType.MANKATO
        else:
            return videoType.OTHER
