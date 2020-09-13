import cv2
from utils import detector_utils as detector_utils

def draw_gui(input_frame, detection_graph, sess, num_hands_detect = 2, score_thresh=0.2):

	height, width, channels = input_frame.shape

	try:
		image_np = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
	except:
		print("Error converting to RGB")

	boxes, scores = detector_utils.detect_objects(image_np,
													detection_graph, sess)

	detector_utils.draw_box_on_image(num_hands_detect, score_thresh,
										scores, boxes, width, height,
										image_np)

	return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)