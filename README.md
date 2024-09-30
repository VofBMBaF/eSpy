<p align="center">
  <img src="https://github.com/user-attachments/assets/c17e4160-06f9-40eb-acd6-e1ba23d15bbe"  />
</p>

## Table of Contents
1. [Introduction](#espy)
2. [Features](#features)
3. [Settings](#settings)
4. [Motion Detection](#motion-detection)
5. [Getting Started](#getting-started)
6. [Prerequisites](#prerequisites)
7. [Cloning the Repository](#cloning-the-repository)
8. [Setting up the App](#setting-up-the-app)
9. [License](#license)
10. [Contact](#contact)


# eSpy

eSpy is a light-weight streaming and recording web application that supports video capture from RTSP cameras, USB sources and webcameras. eSpy is developed with Python and Flask, with a front-end stack consisting of HTML, CSS and JavaScript. It is styled in a dark, modern and minimalistic theme, providing the users easy interface and navigation to manage and monitor live video streams.

It's designed to maintain speed even with larger number of video sources, and comes with an inbuilt motion detection feature using a dynamic, adaptable background subtraction algorithm combined with contour detection which allows the user to adjust the sensitivity of their motion detector as needed depending on the surrounding.

This project offers a glance at the start of a bigger software, with promises that more features are on the way. This project was developed by Vukica Branković as the final project for Harvard's Computer Science course (cs50), combining technologies taught on the course and additional research on computer vision.

Tech Stack:
<b>

* <img src="https://github.com/user-attachments/assets/5be46c01-8d93-428a-b85d-9820d158ab60" width = "20" /> HTML
* <img src="https://github.com/user-attachments/assets/2a652c8c-1dfd-41cd-ae7b-d68d99580dec" width = "20" /> CSS
* <img src="https://github.com/user-attachments/assets/feb1047a-3ca5-45a2-b855-1033d8c66c44" width = "20" /> Bootstrap
* <img src="https://github.com/user-attachments/assets/97813c70-c13f-4a01-b0cc-e8eb0cf60852" width = "20" /> Javascript

*  <img src="https://github.com/user-attachments/assets/cf073de1-5f3d-4f75-acda-cee6362d0ffd" width = "20" /> Python
*  <img src="https://github.com/user-attachments/assets/8a651c78-d028-4c57-981d-00737266999f" width = "20" /> Flask
</b>




## Features

  <b>
    
  * Stream and Record: </b> Stream live video and record footage from multiple video sources. <b>
  * Web Interface: </b> Access and control streams through a web-based interface. <b>
  * Multi-Source Handling:</b> Manage streams from RTSP cameras, USB cameras, and webcams.<b>
  * Configurable Settings:</b> Easily configure video sources and recording options. <b>
  * Persistent data:  </b> In upcoming updates, eSpy will allow users to save their camera sources to their accounts 

   

## Settings

Our minimalistic settings page allows the user to adjust the sensitivity for each camera. It also supports two different recording formats. 

### Sensitivity and Contour Area

For best results, we advise the user to change the sensitivity of the motion detector. 500 is the default value. The value refers to the area of the detected object's contour. If the object is smaller than the certain value, it will be ignored. The user is encouraged to experiment to find the best results and avoid triggering the detector with noise (wind, leaves, rain, birds...etc)

This allows the software to mold to the user's needs, making it friendlier.

## Motion Detection

Our algorithm is designed to dynamically update the background models, combining contour detection to trigger snapshots which are saved to drive into lightweight JPG formats. In future updates, eSpy plans to allow users to make a choice between video clips and snapshots when the algorithm is triggered.

eSpy uses the Python open-source library OpenCV to process videos and images.


## Getting Started

>[!TIP]
>To find the RTSP URL of your camera, we recommend using tools such as AgentDVR url Setup guide or consulting the manufacturer's manual or webpage. Our software DOES NOT offer similar tools of detecting cameras on your network.


## Prerequisites

Before you begin, ensure you have the following software installed:

- **Python**: Version 3.6 or higher. You can download it from [python.org](https://www.python.org/downloads/).
- **Pip**: Python's package installer, which usually comes with Python installations.

## Cloning the Repository

To download the code, open your terminal and run:

```bash
git https://github.com/Vukica-Brankovic/eSpy.git 
```

## Setting up the app

Navigate to project directory

```bash
cd eSpy
```
Install the required packages using pip:

```bash
pip install -r requirements.txt
```
To run the Flask app, use the following command:


```bash
flask run
```
By default, your app will be accessible at http://127.0.0.1:5000/.

>[!IMPORTANT]
> This project is running on the development server without warranty of any kind. The authors are not liable for any issues that arise from using the software. It's up for testing, not secure usage. We encourage users to report all bugs to the administrators. All contributions and tests are welcome and encourages.

## Troubleshooting

If you encounter issues during installation or while running the application, consider the following:

- Ensure you have Python and Pip correctly installed.
- Check for any typos in the command lines.
- If you have any missing packages, try running `pip install -r requirements.txt` again.


## Usage Examples

### Streaming from a USB Camera

1. Obtain the channel of your USB camera (eg. 0 if there is no webcam, 2, 4...)
2. Navigate the menu and enter your channel into the form.
3. Adjust the sensitivity settings as needed.
4. Start streaming!

### Recording Video

To record a video, click on the 'Record'

### Motion Detection

To trigger the motion detector, click on your cameras More menu and navigate to the Motion Detection pop up. Start and enjoy!

### Previewing the files

Saved videos and images will be saved in the project's directory in the subdirectory <b> recordings </b>


## Contact

If you have any questions or would like to get in touch, feel free to reach out:

- **Email**: v.of.bmbaf@gmail.com
- **GitHub**: [Vukica-Brankovic]([https://github.com/yourusername](https://github.com/Vukica-Brankovic))

I welcome feedback and contributions!
  

## Roadmap

- [ ] Implement persistent data storage
- [ ] Add user authentication for personalized settings.
- [ ] Implement secure error handling.
- [ ] Expand the motion detection algorithm for more customizable options.

## Acknowledgments

- [OpenCV](https://opencv.org/)
- [David Malan](https://cs.harvard.edu/malan/)
- [AI Duck Debugger](https://cs50.ai/)




## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




