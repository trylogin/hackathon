import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()


def get_Gaze_Tracking_Coords(frame):
    gaze.refresh(frame)
    Tblink = False

    if gaze.is_blinking():
        Tblink = True
        
    horizontal_ratio_left, horizontal_ratio_right = gaze.horizontal_ratio_double()
    vertical_ratio_left, vertical_ratio_right = gaze.vertical_ratio_double()

    return vertical_ratio_left, horizontal_ratio_left, vertical_ratio_right, horizontal_ratio_right, Tblink
