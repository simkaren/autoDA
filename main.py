import sys, os
import cv2
import threading
import serial
from camera import Camera
from command import commands

def showImage(camera):
    while True:
        frame = cv2.resize(camera.readFrame(), (640, 480))
        cv2.imshow('Video', camera.readFrame())
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

def openSerial(portNum):
	try:
		if os.name == 'nt':
			print('connecting to ' + "COM" + str(portNum))
			ser = serial.Serial("COM" + str(portNum), 115200)
			return True, ser
		elif os.name == 'posix':
			print('connecting to ' + "/dev/ttyUSB" + str(portNum))
			ser = serial.Serial("/dev/ttyUSB" + str(portNum), 115200)
			return True, ser
		else:
			print('not supported OS')
			return False, None
	except IOError as e:
		print('COM Port: can\'t be established')
		print(e)
		return False, None

def main():
    if len(sys.argv) < 3:
        print('Invalid argument(s).')
        return
    camera = Camera()
    cameraOpenSuccess = camera.openCamera(int(sys.argv[1]))
    if not cameraOpenSuccess: return
    serialSuccess, ser = openSerial(int(sys.argv[2]))
    if not serialSuccess: 
        camera.destroy()
        return
    thread_command = threading.Thread(target=commands, args=(camera, ser))
    thread_command.start()
    showImage(camera)

if __name__ == "__main__":
    main()