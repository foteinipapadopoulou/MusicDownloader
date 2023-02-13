from pytube import YouTube


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
        except:
            return 'Error: Failed to fetch url {}'.format(url), 500

        # download into working directory
        try:
            return audio.download(output_path="output"), yt.title
        except:
            return 'Error: Failed to download audio from {}'.format(self.name), 500

    def get_youtube_url_info(self, url):
        try:
            return YouTube(url)
        except Exception as e:
            return e
