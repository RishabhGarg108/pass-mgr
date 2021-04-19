from decouple import config
import numpy as np
import face_recognition
import cv2
import time

ROOT_PASSWORD = config('ROOT_PASSWORD')
KNOWN_EMBEDDINGS = np.load('known_embeddings.npy')
TOLERANCE = 0.6

def authenticatePassword():
    '''Authenticates the user using a text password.'''
    password = input(">>>")
    print('Authenticating master password.')
    return password == ROOT_PASSWORD

def authenticateFace():
    '''Authenticating the user based on face recognition.'''
    cam = cv2.VideoCapture(0)
    auth = False
    start = time.time()
    while True:
        end = time.time()
        # Authenticating for a maximum of 5 seconds.
        if end - start > 5:
            break

        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        frame = cv2.resize(frame, (800, 600))

        unknownEmbeddings = face_recognition.face_encodings(frame)
        if not unknownEmbeddings:
            continue

        results = face_recognition.compare_faces(KNOWN_EMBEDDINGS, unknownEmbeddings, TOLERANCE)

        if True in results:
            auth = True
            break

    cam.release()
    cv2.destroyAllWindows()

    return auth
