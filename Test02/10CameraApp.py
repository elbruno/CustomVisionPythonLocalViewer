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

# Like the CustomVision.ai Prediction service /image route handles either
def predict_image_handler(ImageData):
    try:
        img = Image.open(ImageData)
        results = predict_image(img)
        return jsonify(results)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image', 500


def getPredictionsSorted(jsonPrediction):
  jsonObj = json.loads(jsonPrediction)
  preds = jsonObj['predictions']
  sorted_preds = sorted(preds, key=lambda x: x['probability'], reverse=True)
  strSortedPreds = ""
  if (sorted_preds):
    for pred in sorted_preds:
        # tag name and prob * 100
        tagName     = str(pred['tagName'])
        probability = pred['probability'] * 100
        # apply threshold
        if (probability >= probabilityThreshold):
            strSortedPreds = strSortedPreds + tagName + ": " + str(probability) + "\n"
  return strSortedPreds

# instantiate flask app and push a context
app = Flask(__name__)

# initialize the cv model
initialize()

# init camera
execution_path = os.getcwd()
camera = cv2.VideoCapture(2)
camera_Width  = 640 # 1024 # 1280 # 640
camera_Heigth = 480 # 960 # 780  # 960  # 480
frameSize = (camera_Width, camera_Heigth)

detectionEnabled = False


while True:
    # Init and FPS process
    predSorted = ""
    start_time = time.time()
    fpsInfo = ""
    
    try:
        # Grab a single frame of video
        ret, frame = camera.read()
        img = cv2.resize(frame, (camera_Width, camera_Heigth))

        if  (detectionEnabled):
            # save image to disk and process it
            frameImageFileName = 'image.png'
            cv2.imwrite(frameImageFileName, img)
            r = predict_image_handler(frameImageFileName) #img_data)

            with app.app_context():
                jsonResults = jsonify(r.json())
            jsonStr = jsonResults.get_data(as_text=True)
            predSorted = getPredictionsSorted(jsonStr)

        # calculate FPS >> FPS = 1 / time to process loop
        fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) + "\n-------------------\n" 

    except Exception as e:
        print('EXCEPTION:', str(e))

    # display FPS and Predictions, split text into lines, thanks OpenCV putText()
    frameInfo = fpsInfo + predSorted
    print(frameInfo)

    for i, line in enumerate(frameInfo.split('\n')):
        i = i + 1
        cv2.putText(frame, line, (10, 10 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

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