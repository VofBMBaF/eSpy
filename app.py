import cv2
from datetime import datetime
import os
import time
from flask import Flask, render_template, Response


app = Flask(__name__)

recordings_dir = os.path.join('recordings')
if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)

# List of our camera channels
cameras = [0, 2]

# This function returns the camera with the id of the function's parameter, turned to INT to avoid value errors.
def find_cameras(list_id):
    return cameras[int(list_id)]    

# Store video access in variable

isRecording = False
out = None


# Takes an argument for what camera we want to display
def gen(camera_id):
    # Run forever

    # Takes the argument from the function call
    cam = find_cameras(camera_id)
    # Collects stream from specified camera
    vid = cv2.VideoCapture(cam)
    # Collects width and height of our stream
    frame_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while True:
        time.sleep(0.1)

        # State holds true or false depending on the success of updating frame variable to be a frame from the video stream
        state, frame = vid.read()

        # Break out of while loop when its unsuccesful
        if not state:
            break

        else:

            if isRecording:
                out.write(frame)
            # Flag holds true or false
            # Imencode converts image formats (jpeg here) into streaming data and stores them in memory cache, effectively transforming them into bytes
            flag, buffer = cv2.imencode('.jpg', frame)
            
            # Generator function yields interruptable stream of JPEG bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buffer) + b'\r\n')
    

@app.route('/video_feed/<string:list_id>/')
def video_feed(list_id):

    # Generator function response
    # Passes that id to the gen function so we know what to display to the video feed
    return Response(gen(list_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    

@app.route("/")
def index():
    # camera_list is the amount of cameras we have in the list
    # camera holds all values from cameras 

    return render_template("videos.html", camera_list = len(cameras), cameras = cameras)

@app.route('/start_rec', methods=["POST"])
def start_recording():
    global isRecording, out
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not isRecording:
        fourcc = cv2.VideoWriter_fourcc(*"IYUV")
        out = cv2.VideoWriter(os.path.join(recordings_dir, f'{timestamp}_recording.avi'), fourcc, 20.0, (640, 480))
        isRecording = True
    return '', 203   


        

@app.route('/stop_rec', methods=["POST"])
def stop_recording():

    global isRecording, out
    
    if isRecording:
        out.release()
        isRecording = False
    return '', 203    
