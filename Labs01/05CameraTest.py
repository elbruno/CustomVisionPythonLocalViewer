import cv2
import time

cap = cv2.VideoCapture(1)

# open
i = 0
while True:
    i = i + 1
    start_time = time.time()

    try:
        ret, frame = cap.read()
        img = cv2.resize(frame, (640, 480))

        if (time.time() - start_time ) > 0:
            fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)

        cv2.imshow('@elbruno - Camera Test', img)
    except Exception as e:
        print(f'exc: {e}')
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break