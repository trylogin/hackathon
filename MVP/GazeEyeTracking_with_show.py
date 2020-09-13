import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
Tblinking = 0

def get_Gaze_Tracking_Coords(frame):
    gaze.refresh(frame)
    Tblink = False
    if gaze.is_blinking():
        Tblink = True
    horizontal_ratio_left, horizontal_ratio_right = gaze.horizontal_ratio_double()
    vertical_ratio_left, vertical_ratio_right = gaze.vertical_ratio_double()

    look_right = False 
    look_left = False
    look_down = False
    look_up = False 
    look_center = False

    left_eye = gaze.pupil_left_coords()
    right_eye = gaze.pupil_right_coords()

    if gaze.is_right():
        look_right = True
    if gaze.is_left():
        look_left = True
    if gaze.is_down():
        look_down = True
    if gaze.is_up():
        look_up = True
    if gaze.is_center():
        look_center = True

    return Tblink,horizontal_ratio_left, horizontal_ratio_right, vertical_ratio_left, vertical_ratio_right, left_eye, right_eye, look_right, look_left, look_down, look_up, look_center

# Test Function START
# text = ''
# while True:
#     horizontal_ratio_l = None
#     horizontal_ratio_r = None
#     vertical_ratio_l = None
#     vertical_ratio_r = None

#     _, new_frame = webcam.read()

#     blinked, horizontal_ratio_l, horizontal_ratio_r, vertical_ratio_l, vertical_ratio_r, left, right, look_right, look_left, look_down, look_up, look_center = get_Gaze_Tracking_Coords(frame)

#     if blinked:
#         Tblinking+=1

#     if (left!=None) & (right!=None):
#         xl_coords = left[0]
#         yl_coords = left[1]
#         xr_coords = right[0]
#         yr_coords = right[1]
#         if look_right:
#             xl_coords =xl_coords +25
#             xr_coords =xr_coords +25
#         if look_left:
#             xl_coords =xl_coords - 25
#             xr_coords =xr_coords - 25
#         if look_down:
#             yl_coords =yl_coords - 25
#             yr_coords =yr_coords - 25
#         if look_up:
#             yl_coords = yl_coords+ 25
#             yr_coords = yr_coords+ 25

#     cv2.putText(new_frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
#     #cv2.putText(new_frame, "Blinkings: " + str(Tblinking), (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.4, (147, 58, 31), 1)
#     cv2.putText(new_frame, "Horizontal ratio left: " + str(horizontal_ratio_l), (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.4, (147, 58, 31), 1)
#     # cv2.putText(new_frame, "Horizontal ratio right: " + str(horizontal_ratio_r), (90, 235), cv2.FONT_HERSHEY_DUPLEX, 0.4, (147, 58, 31), 1)
#     cv2.putText(new_frame, "vertical ratio left: " + str(vertical_ratio_l), (90, 235), cv2.FONT_HERSHEY_DUPLEX, 0.4, (147, 58, 31), 1)
#     if (look_center == False):
#         cv2.circle(new_frame, left, 25, (147, 58, 31),3)       
#         cv2.circle(new_frame, right, 25, (147, 58, 31),3)   
#         if (left!=None) & (right!=None):
#             new_frame = cv2.arrowedLine(new_frame, left, (int(xl_coords), int(yl_coords)), (147, 58, 31), 3)
#             new_frame = cv2.arrowedLine(new_frame, right, (int(xr_coords), int(yr_coords)), (147, 58, 31), 3)
#             cv2.putText(new_frame, "pos: " + str(left[0]) + " " + str(left[1]), (90, 305), cv2.FONT_HERSHEY_DUPLEX, 0.4, (147, 58, 31), 1)
#             cv2.putText(new_frame, "new pos: " + str(xl_coords) + " " + str(yl_coords), (90, 335), cv2.FONT_HERSHEY_DUPLEX, 0.4, (147, 58, 31), 1)              
#     cv2.imshow("Demo", new_frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# Test Function END