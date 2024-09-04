import cv2
from datetime import datetime
import os
import time
from flask import Flask, render_template, Response


app = Flask(__name__)

recordings_dir = os.path.join('recordings')
if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)

# Store video access in variable
vid = cv2.VideoCapture(0)
frame_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
isRecording = False
out = None


def gen():
    # Run forever
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
    


@app.route('/video_feed')
def video_feed():

    # Generator function response
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    

@app.route("/")
def index():
    return render_template("videos.html")

@app.route('/start_rec', methods=["POST"])
def start_recording():
    global isRecording, out
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not isRecording:
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
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
