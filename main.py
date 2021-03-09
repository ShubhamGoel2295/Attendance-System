import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from DB_connection import db_connect
# from PIL import ImageGrab

#Finding image path and its class names
path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
# print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0]) # Breaking image names with person name
# print(classNames)

# It is finding Face features
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

'''
# if it is able to identify me then store data in sheet with timing
# For saving the data in excel sheet and mongo db
def markAttendance(name):
    # print(name)
    global count
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        # print(myDataList)
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            # print(entry)
            nameList.append(entry[0])
            # print(len(nameList))
            # print(nameList)
            # count= count+1
            # print(count)
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            dayString = now.strftime('%d-%m-%Y')
            # f.writelines(f'\n{name},{dtString}')
            data_storingDB(name, dtString, dayString)
            print(True)
'''


# Making attendance into DB
def markAttendance(name):
    nameList = []
    nameList= db_object.data_fetchingDB(dbname_list=[])  # first fetching thde records name from DB
    if name.lower() not in nameList:
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        dayString = now.strftime('%d-%m-%Y')
        # f.writelines(f'\n{name},{dtString}')
        db_object.data_storingDB(name, dtString, dayString) # if the person name is not in DM then it will store it
        # print(True)

# Creating DB connection object
db_object= db_connect()

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
# print(name)
            y1, x2, y2, x1 = faceLoc # reactangle box creation above image
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
        # break
