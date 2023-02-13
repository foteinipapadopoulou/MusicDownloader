from pytube import YouTube


class YoutubeProvider:
    def __init__(self, name):
        self.name = name

    def download_audio(self, url):
        # creating YouTube object
        yt = YouTube(url)

        # accessing audio streams of YouTube obj.(first one, more available)
        audio = yt.streams.filter(only_audio=True).first()
        # downloading a video would be: stream = yt.streams.first()

        # download into working directory
        try:
            return audio.download()
        except:
            return 'Error: Failed to download audio from ' + self.name, 500
