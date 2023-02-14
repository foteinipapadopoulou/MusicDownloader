import traceback
from flask import Flask, request, render_template, make_response, jsonify
import requests
import re
import os
import logging

from YoutubeProvider import YoutubeProvider

app = Flask(__name__)
logging.basicConfig(filename='../record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

ALLOWED_HOSTS = [
    "youtube.com",
    "www.youtube.com",
    "youtu.be"
]

def validate_url(url):
    if not (url and url.strip()):
        raise APIBadRequestError('Url value is empty')

    # Check that the link is a valid URL
    if not re.match(r'^https?://.+$', url):
        raise APIBadRequestError('Invalid Url')

    # Check that the link is to an allowed host
    parsed_link = requests.utils.urlparse(url)
    if parsed_link.hostname not in ALLOWED_HOSTS:
        raise APIBadRequestError('Unallowed host in Url. Only Youtube is supported')


class APIError(Exception):
    """All custom API Exceptions"""
    pass


class APIBadRequestError(APIError):
    """Bad Request Error Class."""
    code = 400
    description = "Bad request Error"


class APIInternalServerError(APIError):
    """Internal Server Error Class."""
    code = 500
    description = "Internal Server Error"


@app.errorhandler(APIError)
def handle_exception(err):
    """Return a JSON with response the error message when an APIError is raised"""
    app.logger.error(f"Unknown Exception: {str(err)}")
    app.logger.debug(traceback.format_exc())
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
        app.logger.error(f'{err.description}: {response["message"]}')
    return jsonify(response), err.code


@app.route('/')
def index():
    app.logger.info('Fetching index.html')
    return render_template('index.html')


@app.route('/download_audio', methods=["POST"])
def download_audio():
    if 'url' not in request.form:
        raise APIBadRequestError('Missing url value')
    url = request.form['url']

    validate_url(url)

    # Fetch the audio data from Youtube
    youtube_provider = YoutubeProvider("Youtube")
    try:
        content, title = youtube_provider.download_audio(url=url)
    except Exception as e:
        app.logger.error('Exception : {}'.format(str(e)))
        raise APIInternalServerError('Internal Server Error while downloading music')

    with open(content, 'rb') as f:
        audio_content = f.read()

    # Return the MP3 data as a download
    try:
        response = make_response(audio_content)
    except:
        raise APIInternalServerError('Internal Server Error while returning the response')

    # Remove the data that are stored in the output folder
    try:
        os.remove(content)
    except:
        app.logger.error('Cannot remove the song:{}'.format(content))

    response.headers["Content-Disposition"] = 'attachment; filename="{}.mp3"'.format(title.encode('latin-1', 'ignore'))
    response.headers["Content-Type"] = "audio/mpeg"
    return response, 200


@app.route('/get_audio', methods=["GET"])
def get_audio_title():
    # Get the query parameters from the request
    query_params = request.args
    if 'url' not in query_params:
        raise APIBadRequestError('Missing url value')
    url = query_params.get("url")

    validate_url(url)
    # Fetch the audio data from Youtube
    youtube_provider = YoutubeProvider("Youtube")
    try:
        yt = youtube_provider.get_youtube_url_info(url=url)
    except Exception as e:
        app.logger.error('Exception : {}'.format(str(e)))
        raise APIInternalServerError('Internal Server Error while getting the title')

    title = ""
    # Return the music title
    if yt is not None and hasattr(yt, "title") and yt.title is not None:
        title = yt.title
    else:
        raise APIInternalServerError('Internal Server Error while returning the title')

    return jsonify({"title": "{}".format(title), "status": "success"})


if __name__ == '__main__':
    app.run(debug=True)
