from utils import detector_utils as detector_utils
import cv2
import tensorflow as tf
import argparse
import hands_track_module as htm

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=int, default=0,
	help="path to input video")
args = vars(ap.parse_args())

detection_graph, sess = detector_utils.load_inference_graph()

cap = cv2.VideoCapture(args["input"])

while True:
	(grabbed, frame) = cap.read()

	if not grabbed:
		break
	
	frame = htm.draw_gui(frame, detection_graph, sess)

	cv2.imshow("Demo", frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break