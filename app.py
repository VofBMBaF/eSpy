import cv2
from datetime import datetime
import os
import time
from flask import Flask, render_template, Response, request, redirect


app = Flask(__name__)

recordings_dir = os.path.join('recordings')
if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)

# List of our camera channels
cameras = [0]

# This function returns the camera with the id of the function's parameter, turned to INT to avoid value errors.
def find_cameras(list_id):
    return cameras[int(list_id)]    

# Dictionary to pass recording flags for each camera
recording_states = {}
# Dictionary of video writer objects for each camera
video_writers = {}

# Takes an argument for what camera we want to display
def gen(camera_id):
    # Run forever

    # Finds camera depending on the id inside the list
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

            # get tries to get the value associated with camera_id from the dictionary, if not found, it returns False
            if recording_states.get(cam, False):
                # Find the video writer for that camera and write the frames into it
                video_writers[cam].write(frame)
            # ret holds true or false
            # Imencode converts image formats (jpeg here) into streaming data and stores them in memory cache, effectively transforming them into bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            
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

@app.route('/start_rec/<int:camera_id>', methods=["POST"])
def start_recording(camera_id):

    # Finds camera depending on the id inside the list
    cam = find_cameras(camera_id)

    # Collect global variables
    global recording_states, video_writers

    # Feedback
    print(f"Starting recording for camera {cam}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Checks if camera is not already recording
    if not recording_states.get(cam, False):
        fourcc = cv2.VideoWriter_fourcc(*"IYUV")
        
        # Assign a VideoWriter objct to the cam in the dictionary
        video_writers[cam] = cv2.VideoWriter(os.path.join(recordings_dir, f'{timestamp}_{cam}_recording.avi'), fourcc, 20.0, (640, 480))
        # Set recording to true for this camera
        recording_states[cam] = True
    return '', 203   


        

@app.route('/stop_rec/<int:camera_id>', methods=["POST"])
def stop_recording(camera_id):
    cam = find_cameras(camera_id)

    global recording_states, video_writers
 
    # If it's recording
    if recording_states.get(cam, False):
        # Finalize the file
        video_writers[cam].release()
        # Set recording to false
        recording_states[cam] = False
    return '', 203 


@app.route("/add", methods= ["POST"])
def add_cameras():

    global cameras
    if request.method == "POST":
        channel = request.form.get("channel")
        if not channel:
            print("incorrect channel or blank")
            return 400
        print(f"Here is a channel {channel}")
        channel = int(channel)
        cameras.append(channel)
    return redirect("/")   

@app.route("/remove/<int:camera_id>", methods = ["POST"])
def removeCamera(camera_id):
    cam = find_cameras(camera_id)
    global cameras
    if request.method == "POST":
        if not cam in cameras:
            print("No camera found")
            return "error finding camera", 400
        cameras.remove(cam)
    return redirect("/")   
