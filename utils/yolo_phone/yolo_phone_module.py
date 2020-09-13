#adapted from https://github.com/pjreddie/darknet
import numpy as np
import imutils
import cv2

def phone_detection(input_frame, net, layer_names, input_labels, input_confidence= 0.5, input_threshold= 0.3):
	(H, W) = (None, None)

	frame = input_frame

	if W is None or H is None:
		(H, W) = frame.shape[:2]

	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (608, 608), swapRB=True, crop=False)
	net.setInput(blob)
	layerOutputs = net.forward(layer_names)

	boxes = []
	confidences = []
	classIDs = []

	for output in layerOutputs:
		for detection in output:
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			if confidence > input_confidence:
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	idxs = cv2.dnn.NMSBoxes(boxes, confidences, input_confidence, input_threshold)

	if len(idxs) > 0:
		for i_count in idxs.flatten():
			(x, y) = (boxes[i_count][0], boxes[i_count][1])
			(w, h) = (boxes[i_count][2], boxes[i_count][3])
			if (input_labels[classIDs[i_count]] == "cell phone"):
				text = "PHONE"
				cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 1)

	return frame