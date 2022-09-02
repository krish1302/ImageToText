from flask import Flask
from os.path import join, dirname, realpath
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')

app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

import ImageToText.routes
import ImageToText.model