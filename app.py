import cv2
from flask import Flask, render_template, Response


app = Flask(__name__)

# Store video access in variable
vid = cv2.VideoCapture(0)


def gen():
    # Run forever
    while True:
        # State holds true or false depending on the success of updating frame variable to be a frame from the video stream
        state, frame = vid.read()

        # Break out of while loop when its unsuccesful
        if not state:
            break

        else:
            # Flag holds true or false depending on the success of setting
            # buffer variable to be the the JPEG format of frame
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
    return render_template("index.html")
