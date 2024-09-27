import cv2
from datetime import datetime
import os
import time
from flask import Flask, render_template, Response, request, redirect, jsonify


app = Flask(__name__)

recordings_dir = os.path.join('recordings')
if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)

# List of our camera channels
cameras = [0, 2, 4]


# This function returns the camera with the id of the function's parameter, turned to INT to avoid value errors.
def find_cameras(list_id):
    return cameras[int(list_id)]   

# Dictionary to pass recording flags for each camera
recording_states = {}
detected = {}
# Dictionary to pass motion detection flags for each camera
motion_states = {}
# Dictionary of video writer objects for each camera
video_writers = {}

recordFormat = "avi"
sensitivity = {}

def gen(camera_id):

    global detected, video_writers
    # Finds camera depending on the id inside the list
    cam = find_cameras(camera_id)
    # Collects stream from specified camera
    vid = cv2.VideoCapture(cam)
    detected[cam] = False
       
    val, frame1 = vid.read()
    val, frame2 = vid.read()

    if vid.isOpened():
        while True:
            
            if not val:
                break

            else:

                # get() tries to get the value associated with camera_id from the dictionary, if not found, it returns False
                if recording_states.get(cam, False):                    # Find the video writer for that camera and write the frames into it
                    video_writers[cam].write(frame1)

                if motion_states.get(cam, False):

                    diff = cv2.absdiff(frame1, frame2)
                    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(gray, (5,5), 0)
                    _, tresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
                    dilated = cv2.dilate(tresh, None, iterations=3)
                    eroded = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, (3,3))
                    contours, _ = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    

                    for contour in contours:
                        (x, y, w, h) = cv2.boundingRect(contour)

                        if not sensitivity.get(cam, False):
                            if cv2.contourArea(contour) > 500:

                                continue
                        else: 
                            if cv2.contourArea(contour) > int(sensitivity[cam]):       

                                continue

                        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        try:
                            detected[cam] = True
                            cv2.imwrite(os.path.join(recordings_dir, f'{timestamp}_{cam}.jpg'), frame1)
                       
                        except Exception as e:
                            print(e)  

                # ret holds true or false
                # Imencode converts image formats (jpeg here) into streaming data and stores them in memory cache, effectively transforming them into bytes
                ret, buffer = cv2.imencode('.jpg', frame1)

                frame1 = frame2
                val, frame2 = vid.read()
                
                # Generator function yields interruptable stream of JPEG bytes
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buffer) + b'\r\n')



@app.route('/sensitive/<int:camera_id>', methods = ["POST"])
def sensitive(camera_id):
    cam = find_cameras(camera_id)

    if request.method == "POST":
        global sensitivity
        area = request.form.get("area")
        sensitivity[cam] = area
        print("successfully set new sensitivity area")
    return redirect("/")       



@app.route('/format', methods = ["POST"])
def process_format():

    if request.method == "POST":
        global recordFormat
        format = request.form.get("format")
        recordFormat = format
    return redirect("/")   




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

    return render_template("videos.html", camera_list = len(cameras), cameras = cameras, recording = recording_states)

@app.route('/start_rec/<int:camera_id>', methods=["POST"])
def start_recording(camera_id):

    # Finds camera depending on the id inside the list
    cam = find_cameras(camera_id)

    # Collect global variables
    global recording_states, video_writers, motion_record_states

    # Feedback
    print(f"Starting recording for camera {cam}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Checks if camera is not already recording
    if not recording_states.get(cam, False):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        
        # Assign a VideoWriter objct to the cam in the dictionary
        video_writers[cam] = cv2.VideoWriter(os.path.join(recordings_dir, f'{timestamp}_{cam}_recording.{recordFormat}'), fourcc, 20.0, (640, 480))
        # Set recording to true for this camera
        recording_states[cam] = True

    return '', 203   


@app.route('/detect_motion/<int:camera_id>', methods=["POST"])
def detect_motion(camera_id):
    cam = find_cameras(camera_id)
    global motion_states, video_writers, detected
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not motion_states.get(cam, False):
        motion_states[cam] = True
        #fourcc = cv2.VideoWriter_fourcc(*"IYUV")
        #video_writers[cam] = cv2.VideoWriter(os.path.join(recordings_dir, f'{timestamp}_{cam}_recording.avi'), fourcc, 20.0, (640, 480))
        
    return '', 203   

@app.route('/stop_motion/<int:camera_id>', methods=["POST"])
def stop_motion(camera_id):
    cam = find_cameras(camera_id)
    global motion_states, video_writers

    if motion_states.get(cam, False):
        #video_writers[cam].release()
        motion_states[cam] = False
   
    return jsonify({"success": True}) # Indicate success


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
    return jsonify({"success": True}) # Indicate success

@app.route("/add", methods= ["POST"])
def add_cameras():

    global cameras
    if request.method == "POST":
        channel = request.form.get("channel")
        if not channel:
            return redirect("/")
        
        if not channel == None: 
            channel = int(channel)
            try:
                cameras.append(channel)
            except:
                return 400    
    return redirect("/")   

@app.route("/remove/<int:camera_id>", methods = ["POST"])
def removeCamera(camera_id):

    cam = find_cameras(camera_id)
    global cameras
    if request.method == "POST":
        if not cam in cameras:
            return "error finding camera", 400
        try:
            cameras.remove(cam)
        except:
            return "error removing camera", 400
    return jsonify({"success": True}) # Indicate success
  
