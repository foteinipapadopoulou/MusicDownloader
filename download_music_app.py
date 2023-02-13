from flask import Flask, request, render_template, make_response
import requests
import re
import os
import logging

from YoutubeProvider import YoutubeProvider

app = Flask(__name__)
logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

ALLOWED_HOSTS = [
    "youtube.com",
    "www.youtube.com",
    "youtu.be"
]


@app.route('/')
def index():
    app.logger.info('Fetching index.html')
    return render_template('index.html')


@app.route('/download_audio', methods=["POST"])
def download_audio():
    try:
        url = request.form['url']
    except Exception as e:
        app.logger.error('Exception : {}'.format(str(e)))
        return "Error: request body not correct", 400
    if url is None:
        return "Error: URL not provided", 400
    # Check that the link is a valid URL
    if not re.match(r'^https?://.+$', url):
        return "Error: Invalid URL", 400

    # Check that the link is to an allowed host
    parsed_link = requests.utils.urlparse(url)
    if parsed_link.hostname not in ALLOWED_HOSTS:
        return "Error: Unallowed host", 400

    # Fetch the audio data from Youtube
    youtube_provider = YoutubeProvider("Youtube")
    try:
        content, title = youtube_provider.download_audio(url=url)
    except Exception as e:
        app.logger.error('Exception : {}'.format(str(e)))
        return 'Error: Internal Server Error while downloading music', 500

    with open(content, 'rb') as f:
        audio_content = f.read()

    # Return the MP3 data as a download
    response = make_response(audio_content)

    # Remove the data that are stored in the output folder
    os.remove(content)
    response.headers["Content-Disposition"] = 'attachment; filename="{}.mp3"'.format(title.encode('latin-1', 'ignore'))
    response.headers["Content-Type"] = "audio/mpeg"
    return response, 200


@app.route('/get_audio', methods=["GET"])
def get_audio_title():
    try:
        url = request.form['url']
    except Exception as e:
        app.logger.error('Exception : {}'.format(str(e)))
        return "Error: request body not correct", 400
    if url is None:
        return "Error: URL not provided", 400
    # Check that the link is a valid URL
    if not re.match(r'^https?://.+$', url):
        return "Error: Invalid URL", 400

    # Check that the link is to an allowed host
    parsed_link = requests.utils.urlparse(url)
    if parsed_link.hostname not in ALLOWED_HOSTS:
        return "Error: Unallowed host", 400

    # Fetch the audio data from Youtube
    youtube_provider = YoutubeProvider("Youtube")
    try:
        title = youtube_provider.get_youtube_url_info(url=url)
    except Exception as e:
        app.logger.error('Exception : {}'.format(str(e)))
        return 'Error: Internal Server Error while getting the title', 500

    # Return the music title
    response = make_response(title)
    return response, 200


if __name__ == '__main__':
    app.run(debug=True)
