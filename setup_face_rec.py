import cv2
import os
import numpy as np
import face_recognition


def grabImages(numImages):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("image")

    count = 0
    images = []

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.imshow("image", frame)

        k = cv2.waitKey(1)
        # ESC pressed
        if k % 256 == 27 or count >= numImages:
            print("Escape hit, closing...")
            break

        # SPACE pressed
        elif k % 256 == 32:
            frame = cv2.resize(frame, (800, 600))
            images.append(frame)
            count += 1

    cam.release()
    cv2.destroyAllWindows()
    return np.array(images)


if __name__ == "__main__":
    knownImages = grabImages(5)

    knownEmbeddings = []
    for img in knownImages:
        enc = face_recognition.face_encodings(img)[0]
        knownEmbeddings.append(enc)
        print(enc)

    knownEmbeddings = np.array(knownEmbeddings)

    with open('known_embeddings.npy', 'wb') as f:
        np.save(f, knownEmbeddings)
