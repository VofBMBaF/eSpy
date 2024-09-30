<p align="center">
  <img src="https://github.com/user-attachments/assets/c17e4160-06f9-40eb-acd6-e1ba23d15bbe" />
</p>

# eSpy

eSpy is a light-weight streaming and recording web application that supports video capture from RTSP cameras, USB sources and webcameras. eSpy is developed with Python and Flask, with a front-end stack consisting of HTML, CSS and JavaScript. It is styled in a dark, modern and minimalistic theme, providing the users easy interface and navigation to manage and monitor live video streams.

It's designed to maintain speed even with larger number of video sources, and comes with an inbuilt motion detection feature using a dynamic, adaptable background subtraction algorithm combined with contour detection which allows the user to adjust the sensitivity of their motion detector as needed depending on the surrounding.

This project offers a glance at the start of a bigger software, with promises that more features are on the way. 



## Features

  <b>
    
  * Stream and Record: </b> Stream live video and record footage from multiple video sources. <b>
  * Web Interface: </b> Access and control streams through a web-based interface. <b>
  * Multi-Source Handling:</b> Manage streams from RTSP cameras, USB cameras, and webcams.<b>
  * Configurable Settings:</b> Easily configure video sources and recording options.
  * Persistent data:  <b> In upcoming updates, eSpy will allow users to save their camera sources to their accounts </b>  

   

## Settings

Our minimalistic settings page allows the user to adjust the sensitivity for each camera. It also supports two different recording formats. 

### Sensitivity and Contour Area

For best results, we advise the user to change the sensitivity of the motion detector. 500 is the default value. The value refers to the area of the detected object's contour. If the object is smaller than the certain value, it will be ignored. The user is encouraged to experiment to find the best results and avoid triggering the detector with noise (wind, leaves, rain, birds...etc)

This allows the software to mold to the user's needs, making it friendlier.

## Motion Detection

Our algorithm is designed to dynamically update the background models, combining contour detection to trigger snapshots which are saved to drive into lightweight JPG formats. In future updates, eSpy plans to allow users to make a choice between video clips and snapshots when the algorithm is triggered.

## Getting Started

>[!TIP]
>To find the RTSP URL of your camera, we recommend using tools such as AgentDVR url Setup guide or consulting the manufacturer's manual or webpage. Our software DOES NOT offer similar tools of detecting cameras on your network.



