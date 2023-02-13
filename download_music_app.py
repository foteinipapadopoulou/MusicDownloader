from flask import Flask, request, render_template, make_response
import requests
import re

from YoutubeProvider import YoutubeProvider

app = Flask(__name__)

ALLOWED_HOSTS = [
    "youtube.com",
    "www.youtube.com",
    "youtu.be"
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download_audio', methods=["POST"])
def download_audio():
    try:
        url = request.form['url']
    except:
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

    # Fetch the audio data
    youtube_provider = YoutubeProvider("Youtube")
    try:
        content = youtube_provider.download_audio(url=url)
    except Exception as e:
        return e

    with open(content, 'rb') as f:
        audio_content = f.read()

    # Return the MP3 data as a download
    response = make_response(audio_content)
    response.headers["Content-Disposition"] = "attachment; filename=audio.mp3"
    response.headers["Content-Type"] = "audio/mpeg"
    return response, 200


if __name__ == '__main__':
    app.run(debug=True)
