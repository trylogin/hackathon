import cv2
import os
from modules import service
import GazeEyeTracking_with_show as get_Gaze_Tracking_Coords


def create_final_video_for_student(student):
    
    files = os.listdir(student)
    font = cv2.FONT_HERSHEY_DUPLEX
    font = cv2.FONT_HERSHEY_TRIPLEX

    sql = '''
        SELECT
            main.IMAGE_TIME.IMAGE_PATH,
            main.HEAD_POSITION.X1,
            main.HEAD_POSITION.Y1,
            main.HEAD_POSITION.X2,
            main.HEAD_POSITION.Y2
        FROM
            main.IMAGE_TIME
                INNER JOIN main.HEAD_POSITION
                ON main.IMAGE_TIME.IP = main.HEAD_POSITION.IP
                    AND main.IMAGE_TIME.TIME = main.HEAD_POSITION.TIME
                    
        WHERE
            main.HEAD_POSITION.IP = ?
        ORDER BY
            main.HEAD_POSITION.START DESC,
            main.HEAD_POSITION.TIME
    '''

    conn, cur = service.create_conn()

    cur.execute(sql, (student, ))

    first_bordr = None

    counting_info = [0, 0, 0, 0, 0, 0, 0, 0]

    for row in cur:
        frame = cv2.imread(row[0])

        try:
            if frame == None:
                continue
        except:
            pass

        # frame = cv2.copyMakeBorder(frame, 0, 0, 0, 200, cv2.BORDER_CONSTANT, [255,255,255])
        fff = 350
        bordersize = 0
        frame = cv2.copyMakeBorder(
            frame,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=fff,
            borderType=cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )
        if first_bordr == None:
            out = cv2.VideoWriter(student + '.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 5, (frame.shape[1], frame.shape[0]))
            first_bordr = [0, row[1], row[2], row[3], row[4]]

        cv2.rectangle(frame, (first_bordr[1], first_bordr[2]), (first_bordr[3], first_bordr[4]), (255, 0, 0), frame.shape[1] // 200)

        if row[1] >= first_bordr[1] and row[2] >= first_bordr[2] and row[3] <= first_bordr[3] and row[4] <= first_bordr[4]:
            cv2.rectangle(frame, (row[1], row[2]), (row[3], row[4]), (0, 255, 0), frame.shape[1] // 150)
        else:
            counting_info[6] += 1
            # if row[1] == 0 and row[2] == 0 and row[3] == 0 and row[4] == 0:
            #     cv2.putText(frame, "Face not detected", (frame.shape[1]- fff + 10, 15), font, 0.4, (0, 0, 255), 1)
            # elif row[1] < first_bordr[1] and row[2] < first_bordr[2]:
            #     cv2.putText(frame, "turn your face right and down", (frame.shape[1]- fff + 10, 15), font, 0.4, (0, 0, 255), 1)
            # elif row[1] < first_bordr[1]:
            #     cv2.putText(frame, "turn your face right", (frame.shape[1]- fff + 10, 15), font, 0.4, (0, 0, 255), 1)
            # elif row[2] < first_bordr[2]:
            #     cv2.putText(frame, "turn your face down", (frame.shape[1]- fff + 10, 15), font, 0.4, (0, 0, 255), 1)
            # elif row[3] > first_bordr[3] and row[4] > first_bordr[4]:
            #     cv2.putText(frame, "turn your face left and up", (frame.shape[1]- fff + 10, 15), font, 0.4, (0, 0, 255), 1)
            # elif row[3] > first_bordr[3]:
            #     cv2.putText(frame, "turn your face left", (frame.shape[1]- fff + 10, 15), font, 0.4, (0, 0, 255), 1)
            # elif row[4] > first_bordr[4]:
            #     cv2.putText(frame, "turn your face up", (frame.shape[1]- fff + 10, 15), font, 0.4, (0, 0, 255), 1)
                
            cv2.rectangle(frame, (row[1], row[2]), (row[3], row[4]), (0, 0, 255), frame.shape[1] // 150)

        # show eyes position
        blinked, horizontal_ratio_l, horizontal_ratio_r, vertical_ratio_l, vertical_ratio_r, left, right, look_right, look_left, look_down, look_up, look_center = get_Gaze_Tracking_Coords.get_Gaze_Tracking_Coords(frame)

        counting_info[0] += 1

        if look_left:
            counting_info[1] += 1

        if look_right:
            counting_info[2] += 1

        if look_down:
            counting_info[3] += 1

        if look_up:
            counting_info[4] += 1

        if look_right or look_left or look_up or look_down or left == None or right == None:
            # cv2.putText(frame, "Attention detected shifting gaze", (frame.shape[1]- fff + 10, 50), font, 0.4, (0, 255, 255), 1)
            counting_info[5] += 1

        # cv2.putText(frame, "percent left: " + str(round(counting_info[1] / counting_info[0] * 100)), (frame.shape[1]- fff + 10, 130), font, 0.4, (147, 58, 31), 1)
        # cv2.putText(frame, "percent right: " + str(round(counting_info[2] / counting_info[0] * 100)), (frame.shape[1]- fff + 10, 165), font, 0.4, (147, 58, 31), 1)
        # cv2.putText(frame, "percent up: " + str(round(counting_info[3] / counting_info[0] * 100)), (frame.shape[1]- fff + 10, 200), font, 0.4, (147, 58, 31), 1)
        # cv2.putText(frame, "percent down: " + str(round(counting_info[4] / counting_info[0] * 100)), (frame.shape[1]- fff + 10, 235), font, 0.4, (147, 58, 31), 1)
        cv2.putText(frame, "Penalty points", (frame.shape[1]- fff + 10, 165), font, 0.4, (147, 58, 31), 1)
        cv2.putText(frame, "1. eye: " + str(round(counting_info[5] / counting_info[0] * 100)) + "%", (frame.shape[1]- fff + 10, 200), font, 0.4, (147, 58, 31), 1)
        cv2.putText(frame, "2. head: " + str(round(counting_info[6] / counting_info[0] * 100)) + "%", (frame.shape[1]- fff + 10, 235), font, 0.4, (147, 58, 31), 1)
        cv2.putText(frame, "3. hands: " + str(0) + "%", (frame.shape[1]- fff + 10, 270), font, 0.4, (147, 58, 31), 1)
        cv2.putText(frame, "4. telephone: " + str(0) + "%", (frame.shape[1]- fff + 10, 305), font, 0.4, (147, 58, 31), 1)

        # if look_up or look_left or look_down or look_right:
        #     counting_info[5]

        if left == None and right == None:
            continue

        if (left!=None) & (right!=None):
            xl_coords = left[0]
            yl_coords = left[1]
            xr_coords = right[0]
            yr_coords = right[1]
            if look_right:
                xl_coords =xl_coords +25
                xr_coords =xr_coords +25
            if look_left:
                xl_coords =xl_coords - 25
                xr_coords =xr_coords - 25
            if look_down:
                yl_coords =yl_coords - 25
                yr_coords =yr_coords - 25
            if look_up:
                yl_coords = yl_coords+ 25
                yr_coords = yr_coords+ 25

        if (look_center == False):
            cv2.circle(frame, left, 25, (0, 0, 255),3)       
            cv2.circle(frame, right, 25, (0, 0, 255),3)   
            if (left!=None) & (right!=None):
                # frame = cv2.arrowedLine(frame, left, (int(xl_coords), int(yl_coords)), (147, 58, 31), 3)
                # frame = cv2.arrowedLine(frame, right, (int(xr_coords), int(yr_coords)), (147, 58, 31), 3)
                cv2.arrowedLine(frame, left, (int(xl_coords), int(yl_coords)), (0, 0, 255), 3)
                cv2.arrowedLine(frame, right, (int(xr_coords), int(yr_coords)), (0, 0, 255), 3)
                # cv2.putText(frame, "pos: " + str(left[0]) + " " + str(left[1]), (90, 305), font, 0.4, (147, 58, 31), 1)
                # cv2.putText(frame, "new pos: " + str(xl_coords) + " " + str(yl_coords), (90, 335), font, 0.4, (147, 58, 31), 1)              

        out.write(frame)

    service.close_conn(conn)
    out.release()

create_final_video_for_student('77.43.216.86')