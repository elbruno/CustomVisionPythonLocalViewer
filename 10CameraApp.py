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
                color = (255, 0, 0) 
                thickness = 2                
                cv2.rectangle(img, start_point, end_point, color, thickness)                 
                print(f'start point: {start_point} - end point: {end_point}')
                
    return strSortedPreds

# instantiate flask app and push a context
app = Flask(__name__)

# initialize the cv model
initialize()

# init camera
execution_path = os.getcwd()
camera = cv2.VideoCapture(0)
camera_Width  = 640 # 1024 # 1280 # 640
camera_Heigth = 480 # 960 # 780  # 960  # 480
frameSize = (camera_Width, camera_Heigth)

detectionEnabled = True

while True:
    # Init and FPS process
    predSorted = ""
    start_time = time.time()
    fpsInfo = ""
    
    try:
        # Grab a single frame of video
        ret, frame = camera.read()
        fast_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        img = cv2.resize(fast_frame, (camera_Width, camera_Heigth))

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

    fpsInfo = ""
    if (time.time() - start_time ) > 0:
        fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)

    cv2.imshow('@elbruno - DJI Tello Camera', img)

    # key controller
    key = cv2.waitKey(1) & 0xFF    
    
    if key == ord("d"):
        if (detectionEnabled == True):
            detectionEnabled = False
        else:
            detectionEnabled = True

    if key == ord("q"):
        break

# Release handle to the webcam
camera.release()
cv2.destroyAllWindows()