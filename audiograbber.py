import youtube_dl
from vimeo_downloader import Vimeo
import moviepy.editor as mp
from enum import Enum
import os

class videoType(Enum):
    """Types of supported video links

    Args:
        Enum (videoType): video link type
    """
    YOUTUBE = 0
    VIMEO = 1
    OTHER = 2

class audioGrabber:
    
    __filePath = "" #where resultant audio should be stored
    __fileName = "" #name of final audio file
    __url = ""      #url to be downloaded

    def __init__(self, path, file):
        """initialize instance of audioGrabber

        Args:
            path (string): path to file location
            file (string): final audio file name
        """
        self.__filePath = path
        self.__fileName = file
        if not os.path.isdir(self.__filePath):
            os.mkdir(self.__filePath)

    def __youtube(self, url):
        """helper function that downloads YouTube videos

        Args:
            url (string): link for YouTube video
        """
        fullpath = os.path.join(self.__filePath, self.__fileName)
        video_info = youtube_dl.YoutubeDL().extract_info(url=url,download=False)
        options={'format':'bestaudio/best', 'keepvideo':False,'outtmpl':fullpath,}

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
    
    def __vimeo(self, url):
        """helper function that downloads Vimeo videos

        Args:
            url (string): link to Vimeo video
        """
        v = Vimeo(url)
        stream = v.streams
        stream[-1].download(download_directory=self.__filePath, filename="tmp.mp4")
        clip = mp.VideoFileClip(self.__filePath + "/" + "tmp.mp4")
        fullpath = os.path.join(self.__filePath, self.__fileName)
        clip.audio.write_audiofile(fullpath)
        #os.remove(self.__filePath + "/" + "tmp.mp4") #remove video file

    def dlAudio(self, url):
        """downloads video file (tmp) and extracts audio

        Args:
            url (string): link to video
        """
        self.__url = url
        fullpath = os.path.join(self.__filePath, self.__fileName)
        match self.__videotype(self.__url):
            case videoType.YOUTUBE:
                self.__youtube(self.__url)
            case videoType.VIMEO:
                self.__vimeo(self.__url)
            case videoType.OTHER:
                print("No downloader available for this video type")

    def __videotype(self, url):
        """helper function which parses URL to determine video type

        Args:
            url (string): link to video

        Returns:
            _type_: _description_
        """
        url = url.lower() #remove issues with case sensitivity
        if "youtube" in url:
            return videoType.YOUTUBE
        elif "vimeo" in url:
            return videoType.VIMEO
        else:
            return videoType.OTHER


    