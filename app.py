import cv2
from datetime import datetime
import os
import time
from flask import Flask, render_template, Response
from threading import Thread

class vStream:
    
    # When a class is initialized, we capture a camera from the channel we take as a parameter
    def __init__(self, src):

        self.vid = cv2.VideoCapture(src)

        # Reading first frame
        self.state, self.frame = self.vid.read()

        # Stop flag
        self.stopped = False

    # Function that starts a thread
    def start(self):
        # Passing the get function (effectively collecting frames in the new thread)
        Thread(target=self.get, args=()).start()
        return self
    
    # Function to collect frames
    def get(self):

        while not self.stopped:

            # If reading frame was unsuccesful, stop
            if not self.state:
                self.stop()

            # Else read another frame
            else:
                (self.state, self.frame) = self.vid.read()


    # Function to stop the thread
    def stop(self):
        self.stopped = True

app = Flask(__name__)


recordings_dir = os.path.join('recordings')
if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)

# List of our camera channels
cameras = [0, 2]



# This function returns the camera with the id of the function's parameter, turned to INT to avoid value errors.
def find_cameras(id):
    return cameras[int(id)]    

# Store video access in variable

isRecording = False
isStop = False
out = None

# Takes an argument for what camera we want to display
def gen():

    # Initializes the vStream class with the parameter from the gen function and starts the thread
    video_getter = vStream(0).start()

    while True:
        time.sleep(0.1)

        # Collects the frame from our class
        frame = video_getter.frame

        # Stop flag triggered by a button
        if isStop:
            video_getter.stop()

        # Record flag triggered by a button
        if isRecording:
            out.write(frame)
            # Flag holds true or false
            # Imencode converts image format (jpeg here) into streaming data and stores them in memory cache, effectively transforming them into bytes
        flag, buffer = cv2.imencode('.jpg', frame)
            
            # Generator function yields interruptable stream of JPEG bytes
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buffer) + b'\r\n')
            

    

@app.route('/video_feed/')
def video_feed():

    # Generator function response
    # Passes that id to the gen function so we know what to display to the video feed
    return Response(gen(),
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

@app.route('/stop', methods=["POST"])
def stop():
    global isStop 
    isStop = True
    return '', 203

@app.route('/stop_rec', methods=["POST"])
def stop_recording():

    global isRecording, out
    
    if isRecording:
        out.release()
        isRecording = False
    return '', 203    

