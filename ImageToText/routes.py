from ImageToText import app
from flask import flash, request, redirect, url_for, render_template, Response
import cv2
from ImageToText.model import mysql
import os
from werkzeug.utils import secure_filename
from ImageToText.newone.text_detection import main

def createCursor():
    cursor = mysql.connection.cursor()
    return cursor

def commit():
    return  mysql.connection.commit()

@app.route('/')
def home():
    camera = ""
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    user_name = request.form.get('uname')
    password = request.form.get('psw')
    try:
        cursor = createCursor()
        cursor.execute('INSERT INTO `user_table`(`user_email`, `user_password`) VALUES (%s,%s)',(user_name,password))
        commit()
        return render_template('login.html')
    except Exception as e:
        return render_template('login.html', signup= 'yes', signup_error= 'user already exist')

    

@app.route('/login',methods=['POST'])
def login():
    user_name = request.form.get('uname')
    password = request.form.get('psw')

    cursor = createCursor()
    cursor.execute('SELECT * FROM `user_table` WHERE `user_email` = %s',[user_name])
    data = cursor.fetchone()
    commit()
    if data[1] == password:
        return redirect('/index')
    else:
        return render_template('login.html',login_error = "username or password not match")

@app.route('/index')
def index():
    return render_template('index.html')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS_VIDEO = set(['mp4', 'avi', 'mkv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO

@app.route('/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
	    return render_template('index.html')
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', data = file.filename)

@app.route('/video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
	    return render_template('index.html')
    file = request.files['file']
    if file and allowed_video(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', data = file.filename)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


def createCamera():
    while True:
        camera = cv2.VideoCapture(0)  
        return camera



def gen_frames():  # generate frame by frame from camera
    camera = createCamera()
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    print('okay')
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(main('live'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_close')
def video_close():
    return "Hello world"

@app.route('/video_detected/<filename>')
def video_detected(filename):
    if filename == 'live':
        print('live video')  
        return Response(main(''), mimetype='multipart/x-mixed-replace; boundary=frame')
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(main(app.config['UPLOAD_FOLDER']+'/'+filename), mimetype='multipart/x-mixed-replace; boundary=frame')
