import cv2

def code_decode(signal):
	return {"left_eyes": "eyes moved to left",
			"right_eyes": "eyes moved to right",
			"up_eyes": "eyes moved to up",
			"down_eyes": "eyes moved to down",
			"face_out": "face out of box",
			"hand_out": "one hand doesn't detected",
			"hands_out": "both hands doesn't detected",
			"phone_detected": "phone detected"}.get(signal, -1)    

def menu(img, height, width, warning):
	overlay = img.copy()
	cv2.rectangle(overlay, (int(width - width/4), 0), (width, height) , (38, 35, 32), cv2.FILLED)
	overlay = cv2.line(overlay, (int(width - width/4 + 30), 95), (int(width - 30), 95), (85, 85, 85), 1)
	alpha = 0.85
	image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
	image_new = cv2.line(image_new, (int(width - width/4), 0), (int(width - width/4), height), (18, 15, 12), 1) 

	font_size = 0.5

	cv2.putText(image_new, "Command: " + "Turn your face right", (int(width - width/4 + 5),35), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0,75,185), 2)
	if (warning!=-1):
		cv2.putText(image_new, "WARNING, " + warning, (int(width - width/4 + 5),70), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0,35,185), 2)
	else:
		cv2.putText(image_new, "No warnings", (int(width - width/4 + 5),70), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0,185,0), 1)

	cv2.putText(image_new, "Percent Left: ",(int(width - width/4 + 15),140), cv2.FONT_HERSHEY_SIMPLEX, font_size, (180, 180, 180), 1)
	cv2.putText(image_new, "Percent Right: ",(int(width - width/4 + 15),175), cv2.FONT_HERSHEY_SIMPLEX, font_size, (180, 180, 180), 1)
	cv2.putText(image_new, "Percent Up: ",(int(width - width/4 + 15),210), cv2.FONT_HERSHEY_SIMPLEX, font_size, (180, 180, 180), 1)
	cv2.putText(image_new, "Percent Down: ",(int(width - width/4 + 15),245), cv2.FONT_HERSHEY_SIMPLEX, font_size, (180, 180, 180), 1)

	return image_new

def draw_bbox(img, label, signal):

	warning = code_decode(signal)
	height, width, channels = img.shape

	rect_h = int(height/20)
	rect_w = int(width/20)
	center = (int(rect_h/2), int(rect_w/2))

	if rect_h>=64:
		font_size = 2
	else:
		font_size = 1

	if (len(str(label)) > 2):
		rect_w = rect_w + (int(rect_w/4)*len(str(label)))
		text = str(label)
	elif (label<=9):
		text = "0" + str(label)
	else:
		text = str(label)

	cv2.rectangle(img, (0,0), (rect_w,rect_h), (255,255,255),-1)
	cv2.rectangle(img, (0,0), (rect_w,rect_h), (0,0,0),2)

	cv2.putText(img, text, center, cv2.FONT_HERSHEY_SIMPLEX, font_size, (0,0,0), 2)
	img = menu(img, height, width, warning)
	return img