import os
import cv2
import argparse
import yolo_phone_module as ypm

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=int, default=0,
	help="path to input video")
ap.add_argument("-y", "--yolo", default='data',
	help="base path to YOLO directory")
args = vars(ap.parse_args())

labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
labels = open(labelsPath).read().strip().split("\n")

weightsPath = os.path.sep.join([args["yolo"], "Fyolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "Fyolov3.cfg"])

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
layer_names = net.getLayerNames()
layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

cap = cv2.VideoCapture(args["input"])

while True:
	(grabbed, frame) = cap.read()

	if not grabbed:
		break

	frame = ypm.phone_detection(frame, net, layer_names, labels)

	cv2.imshow("Demo", frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break