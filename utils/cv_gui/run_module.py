import cv2
import argparse
import highlight_gui as hg

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=int, default=0,
	help="path to input video")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["input"])

i_count = 985

while True:
	(grabbed, frame) = cap.read()

	if not grabbed:
		break
	
	i_count += 1

	frame = hg.draw_bbox(frame, i_count, "hands_out")
	cv2.imshow("Demo", frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break