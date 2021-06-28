# FaceRec Imports
import os
import cv2
import face_recognition as fr
import numpy as np
from time import sleep
import numpy as np

#Roast Imports
from insults import Insults
import time
import random
import pyttsx3

def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        print(fnames)
        for num, f in enumerate(fnames):
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded

def classify_face_video(frame, faces_encoded, known_face_names):
    """
    Will take in a frame and return names and locations of faces 
    """
    face_locations = fr.face_locations(frame)
    unknown_face_encodings = fr.face_encodings(frame, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown1"

        # use the known face with the smallest distance to the new face
        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
    
    return face_locations, face_names


# CV2 Video Cap and Face Detection
cap = cv2.VideoCapture(0)
running = True
faces_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Loads in Insults
insults = Insults()
insult_time = time.time()
insult_timer = 5
engine = pyttsx3.init()

# Gets Test Faces
faces = get_encoded_faces()
faces_encoded = list(faces.values())
known_face_names = list(faces.keys())

while running:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faces_cascade.detectMultiScale(gray, 1.05, 10)
    face_names = []
    
    # Check Faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #roi_gray = gray[y:y+h, x:x+w]
        buffer = 50
        roi_color = frame[y-buffer:y+h+buffer, x-buffer:x+w+buffer]
        loc, name = classify_face_video(roi_color, faces_encoded, known_face_names)
        if len(name) < 1:
            name = ["Unknown2"]
        face_names.append(name)

    if time.time() - insult_time > insult_timer:
        #Insult Determination
        if len(face_names) > 0: # If face in frame, then insult
            # Needs Improvement
            known_faces = []
            for name in face_names:
                if name != "Unknown1" or name != "Unknown2":
                    known_faces.append(name)
            if len(known_faces) > 0: known = True
            
            rand = random.randint(1,10)
            if rand <= 7: #Long Insult
                if known and rand <= 4: # Peronal insult
                    chosen_name = known_faces[random.randint(0, len(known_faces) - 1)]
                    chosen_insult = insults.personal_insults[chosen_name][random.randint(0, len(insults.personal_insults[chosen_name] - 1))]
                else: # Non-personal Insult
                    chosen_insult = insults.long_insults[random.randint(0, len(insults.long_insults) - 1)]
            else: #Short Insult
                short = insults.short_insults[random.randint(0, len(insults.short_insults) - 1)]
                if known:
                    chosen_insult = insults.known_short_setups(known_faces[random.randint(0, len(known_faces) - 1)])
                else:
                    chosen_insult = insults.unknown_short_setups()
        
            # TTS code
            engine.say(chosen_insult)
            engine.runAndWait()
            # Resets Insult Variables
            insult_time = time.time()
            insult_timer = random.randint(5, 15)
    

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()
