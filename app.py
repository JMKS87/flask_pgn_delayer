import os
import time

from cachetools import TTLCache, cached
from flask import Flask, request, send_from_directory

DIR = os.path.dirname(os.path.abspath(__file__))
FILES = os.path.join(DIR, 'FILES')
ALLOWED_EXTENSIONS = {'pgn'}
DELAY = 2 * 60  # 2 minutes
DOWNLOAD_CACHE_TIME = 10  # seconds

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file provided!', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file!', 400
    if file and allowed_file(file.filename):
        filename = f"{int(time.time())}.pgn"
        file.save(os.path.join(FILES, filename))
        return ""


@cached(cache=TTLCache(maxsize=1, ttl=DOWNLOAD_CACHE_TIME))
@app.route('/download', methods=['GET'])
def download():
    current_time = int(time.time())
    max_timestamp = current_time - DELAY
    files = sorted([filename for filename in os.listdir(FILES) if filename.endswith('.pgn')], reverse=True)
    selected_file = None
    for file in files:
        try:
            current_file_timestamp = int(file[:-4])
        except ValueError:
            pass
        else:
            if current_file_timestamp < max_timestamp:
                selected_file = file
                break
        selected_file = file
    if not selected_file:
        return 'No file found!', 500
    return send_from_directory(FILES, selected_file)




if __name__ == '__main__':
    app.run(host='0.0.0.0')
