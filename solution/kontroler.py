from flask import Flask, json
from test2 import audio_predict
from flask_cors import CORS
from flask import request
from test2 import audio_predict
import os

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
UPLOAD_FOLDER = os.getcwd() + '/save'

api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(api)

@api.route('/companies', methods=['POST'])
def get_companies():
  file = request.files['file']
  file.save(os.path.join(api.config['UPLOAD_FOLDER'], 'test1.wav'))
  return audio_predict(api.config['UPLOAD_FOLDER'], 'test1.wav')

if __name__ == '__main__':
    api.run()
