#    Copyright (c) 2023
#    Author      : Bruno Capuano
#    Change Log  :
#       - Open a local camera using OpenCV
#       - Load a image recognition model created using CustomVision.ai
#       - Detect objects in the camera frame
#       - Display the detected objects in the camera frame
#       - Display the FPS (Frames Per Second) in the camera frame
#       - Display the detected objects in the camera frame
#       - Manage the app with the following keys:
#           - Press D to enable or disable the detection
#           - Press L to show or hide the labels
#           - Press F to show or hide the FPS
#           - Press Q to exit
#
#    The MIT License (MIT)
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.

import os
import cv2
import time
import urllib
import json
import requests
import io

# Imports for the REST API
from flask import Flask, request, jsonify

# Imports for image procesing
from PIL import Image

# Imports for prediction
from predict import initialize, predict_image, predict_url

probabilityThreshold = 15

def displayPredictions(jsonPrediction, frame):

    global camera_Width, camera_Heigth
    jsonObj = json.loads(jsonPrediction)
    preds = jsonObj['predictions']
    sorted_preds = sorted(preds, key=lambda x: x['probability'], reverse=True)
    strSortedPreds = ""
    resultFound = False
    if (sorted_preds):
        for pred in sorted_preds:
            # tag name and prob * 100
            tagName     = str(pred['tagName'])
            probability = pred['probability'] * 100
            #print(f'{tagName} - {probability}')

            # apply threshold
            if (probability >= probabilityThreshold):
                print(f'{tagName} - {probability}')

                bb = pred['boundingBox']

                # adjust to size
                height = int(bb['height'] * camera_Heigth)
                left = int(bb['left'] * camera_Width)
                top = int(bb['top'] * camera_Heigth)
                width = int(bb['width'] * camera_Width)

                # draw bounding boxes
                start_point = (left, top)                 
                end_point = (left + width, top + height) 
                thickness = 2                
                cv2.rectangle(img, start_point, end_point, colorDetected, thickness)                 
                print(f'start point: {start_point} - end point: {end_point}')

                if displayLabels:
                    # format probability with no decimals
                    probability = "{:.0f}%".format(probability)                    
                    label = f'{tagName} - {probability}'
                    cv2.putText(img, label, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, colorDetected, 1, cv2.LINE_AA)
                
    return strSortedPreds

# instantiate flask app and push a context
app = Flask(__name__)

# initialize the cv model
initialize()

# init camera
execution_path = os.getcwd()
camera = cv2.VideoCapture(0)
camera_Width  = 640 # 1024 # 1280 # 640
camera_Heigth = 480 # 780  # 960  # 480
frameSize = (camera_Width, camera_Heigth)

detectionEnabled = False
displayLabels = False
displayFPS = False

# create color detected as White
colorDetected = (255, 255, 255)

while True:
    # Init and FPS process
    predSorted = ""
    start_time = time.time()
    fpsInfo = ""
    
    try:
        # Grab a single frame of video
        ret, frame = camera.read()
        img = cv2.resize(frame, frameSize)

        # this lower the quality of the image for slower devices
        #fast_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #img = cv2.resize(fast_frame, frameSize)

        if  (detectionEnabled):
            # save image to disk and process it
            frameImageFileName = 'image.png'
            cv2.imwrite(frameImageFileName, img)

            imgPil = Image.open(frameImageFileName)
            results = predict_image(imgPil)
            json_results = ""
            with app.app_context():        
                 json_results = jsonify(results)          
                 json_results = json_results.response[0]
            predSorted = displayPredictions(json_results, img)

    except Exception as e:
        print('EXCEPTION:', str(e))

    if displayFPS:
        fpsInfo = ""
        if (time.time() - start_time ) > 0:
            fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, fpsInfo, (10, 20), font, 0.4, colorDetected, 1)

    cv2.imshow('El Bruno - CV Viewer', img)

    # key controller
    key = cv2.waitKey(1) & 0xFF    
    
    if key == ord("d"):
        if (detectionEnabled == True):
            detectionEnabled = False
        else:
            detectionEnabled = True

    if key == ord("f"):
        if (displayFPS == True):
            displayFPS = False
        else:
            displayFPS = True

    if key == ord("l"):
        if (displayLabels == True):
            displayLabels = False
        else:
            displayLabels = True

    if key == ord("q"):
        break

# Release handle to the webcam
camera.release()
cv2.destroyAllWindows()