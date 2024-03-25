from pytube import YouTube

from src.error import APIInternalServerError


class YoutubeProvider:
    def __init__(self, name):
        self.name = name

    def download_audio(self, url):
        # creating YouTube object
        try:
            yt = self.get_youtube_url_info(url)
            # accessing audio streams of YouTube obj.(first one, more available)
            audio = yt.streams.filter(only_audio=True).first()
            # downloading a video would be: stream = yt.streams.first()
            return audio.download(), yt.title
        except Exception as e:
            raise APIInternalServerError('Internal Server Error while downloading music {}'.format(str(e)))

    def get_youtube_url_info(self, url):
        try:
            return YouTube(url)
        except Exception as e:
            return e
