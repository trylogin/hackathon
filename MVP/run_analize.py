import cv2
import GazeEyeTracking
import os
import dlib

from modules import service
from datetime import datetime
from modules.faces import Face_Detector
from shutil import copyfile


detector = Face_Detector()

folder_name = '77.43.216.86'

frames = os.listdir(folder_name)

try:
    os.remove('results.db')
except:
    print('db wasnt ermoved')

try:
    copyfile('clear_results.db', 'results.db')
except:
    print('cant copy db')

for frame_name in frames:
    # определение положения зрачков
    frame = cv2.imread(folder_name + '/' + frame_name)

    try:
        if frame == None:
            continue
    except:
        pass

    coords = GazeEyeTracking.get_Gaze_Tracking_Coords(frame)
    
    conn, cur = service.create_conn()
    create_time = os.path.getctime(folder_name + '/' + frame_name)
    create_datetime = datetime.fromtimestamp(create_time)

    try:
        cur.execute('INSERT INTO EYES_MOVEMENT VALUES(?, ?, ?, ?, ?, ?)', (folder_name, create_datetime, coords[0], coords[1], coords[2], coords[3]))
    except:
        pass

    try:
        cur.execute('INSERT INTO IMAGE_TIME VALUES(?, ?, ?)', (folder_name, create_datetime, folder_name + '/' + frame_name))
    except:
        pass

    service.close_conn(conn)

conn, cur = service.create_conn()

cur.execute('SELECT * FROM IMAGE_TIME WHERE IP=? ORDER BY TIME', (folder_name, ))

first_frame = ""

for row in cur:
    first_frame = row[2]
    break

service.close_conn(conn)

for frame_name in frames:
    # определение положения головы
    start = 0
    frame = cv2.imread(folder_name + '/' + frame_name)

    try:
        if frame == None:
            continue
    except:
        pass

    create_time = os.path.getctime(folder_name + '/' + frame_name)
    create_datetime = datetime.fromtimestamp(create_time)

    if folder_name + '/' + frame_name == first_frame:
        start = 1

    if start == 1:
        without_error, face = detector.detect(frame, 1)
    else:
        without_error, face = detector.detect(frame, 0)

    position = {
        'x1': 0,
        'y1': 0,
        'x2': 0,
        'y2': 0
    }

    if without_error:
        position['x1'] = face[0].region[0]
        position['y1'] = face[0].region[1]
        position['x2'] = face[0].region[2]
        position['y2'] = face[0].region[3]

    conn, cur = service.create_conn()

    try:
        cur.execute('INSERT INTO HEAD_POSITION VALUES(?, ?, ?, ?, ?, ?, ?)', (folder_name, create_datetime, position['x1'], position['y1'], position['x2'], position['y2'], start))
    except:
        pass

    service.close_conn(conn)