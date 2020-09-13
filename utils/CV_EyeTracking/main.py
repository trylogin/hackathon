import cv2
import numpy as np


# init part
face_cascade = cv2.CascadeClassifier('src/models/haar/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('src/models/haar/haarcascade_eye.xml')
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)


def detect_faces(img, cascade):
    coords = cascade.detectMultiScale(img, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
    return frame


def detect_eyes(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
    width = np.size(img, 1)  # get face frame width
    height = np.size(img, 0)  # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]
    return left_eye, right_eye


def cut_eyebrows(img):
    height, width = img.shape[:2]
    img = img[15:height, 0:width]  # cut eyebrows out (15 px)

    return img


# def blob_process(img, threshold, detector):
#     gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
#     img = cv2.erode(img, None, iterations=2)
#     img = cv2.dilate(img, None, iterations=4)
#     #img = cv2.medianBlur(img, 3)
#     cv2.imshow('test', img)
#     keypoints = detector.detect(img)
#     print(keypoints)
#     return keypoints

def blob_process(img, threshold, erode,dilate, detector, prevArea=None):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray_frame = img
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=erode) #2
    img = cv2.dilate(img, None, iterations=dilate) #4
    #img = cv2.medianBlur(img, 5) #5
    cv2.imshow('test', img)
    keypoints = detector.detect(img)

    if keypoints and prevArea and len(keypoints) > 1:
        tmp = 1000
        for keypoint in keypoints:  # filter out odd blobs
            if abs(keypoint.size - prevArea) < tmp:
                ans = keypoint
                tmp = abs(keypoint.size - prevArea)
        keypoints = np.array(ans)

    return keypoints

def nothing(x):
    pass

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.namedWindow('test')
    cv2.createTrackbar('threshold', 'image', 0, 255, nothing)
    cv2.createTrackbar('erode', 'image', 0, 255, nothing)
    cv2.createTrackbar('dilate', 'image', 0, 255, nothing)
    cv2.createTrackbar('medianBlur', 'image', 3, 255, nothing)
    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (800, 600))
        face_frame = detect_faces(frame, face_cascade)
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    threshold = r = cv2.getTrackbarPos('threshold', 'image')
                    erode = r = cv2.getTrackbarPos('erode', 'image')
                    dilate = r = cv2.getTrackbarPos('dilate', 'image')
                    eye = cut_eyebrows(eye)
                    keypoints = blob_process(eye, threshold,erode,dilate, detector)
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()