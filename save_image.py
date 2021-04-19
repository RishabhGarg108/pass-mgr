import cv2
import os
import numpy as np

directory = "data"
path = os.path.join(os.getcwd(), directory)
try:
    os.mkdir(path)
except:
    print("Directory already exists!")

os.chdir(path)



def grabImages():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("image")

    count = 0
    images = []

    while count < 5:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.imshow("image", frame)

        k = cv2.waitKey(1)
        # ESC pressed
        if k % 256 == 27:
            print("Escape hit, closing...")
            break

        # SPACE pressed
        elif k % 256 == 32:
            images.append(frame)
            count += 1

    cam.release()
    cv2.destroyAllWindows()
    return np.array(images)

images = grabImages()