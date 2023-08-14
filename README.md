# Azure Custom Vision - Local model viewer Sample

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE)
[![Twitter: elbruno](https://img.shields.io/twitter/follow/elbruno.svg?style=social)](https://twitter.com/elbruno)
![GitHub: elbruno](https://img.shields.io/github/followers/elbruno?style=social)

_Create an object detection model in Azure Custom Vision, and running locally in minutes._ ✨

This is a sample project to use a object detection model, created using  [Azure Custom Vision](https://customvision.ai), locally in a desktop application. 

In order to test the plugin you need access to the ChatGPT plugins developer program. To gain access to ChatGPT plugins, [join waitlist here](https://openai.com/waitlist/plugins)!


## Prerequisites

1. **🐍 Anaconda**

    Download and install the latest version of [Anaconda](https://www.anaconda.com/).
1. **🪄 Create a local virtual environment**

    Open Anaconda PowerShell Prompt.
    Run the following commands to create a virtual environment named [demo]

    ```bash
    conda create -n demo python=3.7
    conda activate demo
    ```
    
    Once the virtual env is activated the PowerShell window must show the (demo) env.

1. **▶️ Install project dependencies**: 

    Run the following commands to install the required dependencies.

    ```bash
    # install latest version of OpenCV
    pip install opencv-python
    ```

    ```bash
    # Install tensorflow and general dependencies
    pip install --no-cache-dir numpy~=1.17.5 tensorflow~=2.0.2 flask~=2.1.2 pillow~=7.2.0 protobuf~=3.20.0
    ```
    
    ```bash
    # Install image processing library
    pip install --no-cache-dir mscviplib
    ```

    The environment is ready to be used.

1. The file `00CheckEnv.py` will test if all the requirements are sucessfully installed.

1. Run the check environment file with the command.

    ```bash    
    python .\00CheckEnv.py
    ```

1. The output should be similar to this one:

    ```bash    
    TensorFlow: 2.0.4
    OpenCV: 4.8.0
    ```

## Download the Custom Vision model

1. Once you have you model trained, export and download a Docker Linux version of the model.

    ![Export model to Docker Linux](/img/cvdownloadlinux.png "Export model to Docker Linux")

2. Extract the model and, from the app folder, copy the following files to the root of this repository.
    - labels.txt
    - model.pb
    - predict.py

## Select the right Camera

1. The file `05CameraTest.py` will allow us to identify the right camera to use. Edit the file and change  the number in the line [cap = cv2.VideoCapture(0)] until the right camera is in use.

    ```python
    import cv2
    import time

    # access to the camera, change the index to use the right camera
    cap = cv2.VideoCapture(0)
    ```

1. Run the file `05CameraTest.py` with the command.

    ```bash    
    python .\05CameraTest.py
    ```

## Run Locally

1. The file `10CameraApp.py` will use the camera and the exported model to detect object and display the objects in a window. Update the file to use the right.

1. Run the app with the command.

    ```bash    
    python .\10CameraApp.py
    ```

1. Once the app is running, you can press the following keys to enable / disable some features.
    - Press D to enable or disable the detection
    - Press L to show or hide the labels
    - Press F to show or hide the FPS
    - Press Q to exit


1. This is an example of the app running.

    ![Detecting Captain America Shield and Cancer Sign](/img/objectdetected.png "Detecting Captain America Shield and Cancer Sign")

## Author

👤 **Bruno Capuano**

* Website: https://elbruno.com
* Twitter: [@elbruno](https://twitter.com/elbruno)
* Github: [@elbruno](https://github.com/elbruno)
* LinkedIn: [@elbruno](https://linkedin.com/in/elbruno)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/elbruno/OpenAI-Plugin-NET-Sample/issues).

## Show your support

Give a ⭐️ if this project helped you!


## 📝 License

Copyright &copy; 2023 [Bruno Capuano](https://github.com/elbruno).

This project is [MIT](/LICENSE) licensed.

***