import sys, os
import cv2
import time, datetime

class Camera:
	def __init__(self):
		self.camera = None
		self.capture_size = (1280, 720)
		self.capture_dir = "Captures"

	def openCamera(self, cameraId):
		if self.camera is not None and self.camera.isOpened():
			self.destroy()

		if os.name == 'nt':
			self.camera = cv2.VideoCapture(cameraId, cv2.CAP_DSHOW)
		else:
			self.camera = cv2.VideoCapture(cameraId)

		if not self.camera.isOpened():
			print("Camera ID " + str(cameraId) + " can't open.")
			return False
		print("Camera ID " + str(cameraId) + " opened successfully")
		self.camera.set(cv2.CAP_PROP_FPS, 60)
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_size[0])
		self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_size[1])
		return True

	def isOpened(self):
		return self.camera.isOpened()

	def readFrame(self):
		_, self.image_bgr = self.camera.read()
		return self.image_bgr
	
	def saveCapture(self, name=''):
		dt_now = datetime.datetime.now()

		filename = dt_now.strftime('%Y-%m-%d_%H-%M-%S') if len(str(name)) == 0 else name
		ext = '.png'
		path = str(filename) + ext

		if not os.path.exists(self.capture_dir):
			os.makedirs(self.capture_dir)

		save_path = os.path.join(self.capture_dir, path)
		cv2.imwrite(save_path, self.image_bgr)
		print('capture succeeded: ' + save_path)
		return save_path

	def destroy(self):
		if self.camera is not None and self.camera.isOpened():
			self.camera.release()
			self.camera = None
	
	def isContainTemplate(self,
		template_path, threshold=0.7, use_gray=True, show_value=False,
		area=[], tmp_area=[]):
		threshold -= 0.1
		src = self.readFrame()
		src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if use_gray else src

		template = cv2.imread('./Template/'+template_path, cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)
		w, h = template.shape[1], template.shape[0]

		method = cv2.TM_CCOEFF_NORMED
		res = cv2.matchTemplate(src, template, method)
		_, max_val, _, max_loc = cv2.minMaxLoc(res)

		if max_val > threshold:
			if use_gray:
				src = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

			top_left = max_loc
			bottom_right = (top_left[0] + w, top_left[1] + h)
			cv2.rectangle(src, top_left, bottom_right, (255, 0, 255), 2)
			return True
		else:
			return False