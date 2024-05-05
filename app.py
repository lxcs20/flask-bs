import os
from flask import Flask, jsonify, request, redirect, flash, url_for, send_from_directory
from markupsafe import escape
from werkzeug.utils import secure_filename

import datetime
import json

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users = []


@app.route("/helloworld")
def helloworld():
    return "Hello World!"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(app.config['UPLOAD_FOLDER'])
            _filename = str(datetime.datetime.now().timestamp()).split('.')[1] + filename
            file.save(f'{UPLOAD_FOLDER}/{_filename}')
            return redirect(url_for('download_file', name=_filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    print(f'file name: {name}')
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# send data via body
@app.post("/user")
def create_user():
    user_byte: bytes = request.get_data()
    user_json = user_byte.decode()
    print(json.loads(user_json))
    users.append(json.loads(user_json))
    return user_json

@app.get("/user")
def get_user():
    print('user:', users)
    return users #[json.loads(user) for user in users]


@app.post("/text")
def get_text():
    text = request.get_data()
    return text
    