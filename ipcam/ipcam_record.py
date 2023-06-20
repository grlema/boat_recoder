#!/usr/bin/env python3
import cv2
import time, sys
import numpy as np
import argparse
import threading

parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='IP Camera address and port, EX. --ip 192.168.1.100:8080')
args = parser.parse_args()
if args.ip == None:
    print('Error!! Please set the IP:port!')
    sys.exit()
ip_addr = 'http://' + args.ip

class ipcam_Capture:
    def __init__(self, URL):
        global width, height, fps
        self.frame = []
        self.status = False
        self.isstop = False

        # connecting camera
        self.cap = cv2.VideoCapture(URL)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print("Width=", width, "Height=", height, "FPS=", fps)

    def start(self):
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        self.isstop = True
        print('Stop record!')

    def getframe(self):
        return self.Frame.copy()

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.cap.read()

        self.cap.release()
# connecting camera
cam = ipcam_Capture(ip_addr)
# start threading
cam.start()
# waiting 1sec
time.sleep(1)
# set record file path
if sys.platform == 'win32':
    path = '.\\recording\\'
else:
    path = './recording/'

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # (*'XVID')
localtime = time.localtime()
path_file = path + time.strftime("%Y%m%d-%H%M%S", localtime) + '.mp4'
min = localtime.tm_min
# print(path_file)
record_fps = 15
r_f = 1
img = cam.getframe()
img=cv2.resize(img, (int(width*0.8), int(height*0.8)), interpolation=cv2.INTER_LINEAR)
cv2.imshow('Streaming', img)
out = cv2.VideoWriter(path_file, fourcc, record_fps, (width, height))
print("Start recording!")
while True:
    img = cam.getframe()
    # ---------- Display Time in imshow
    localtime = time.localtime()
    min_next = localtime.tm_min
    sec_next = localtime.tm_sec
    # print(r_f, min,min_next,':',sec_next)
    eventtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    cv2.putText(img, eventtime, (10, height - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (30, 57, 181), 2, cv2.LINE_AA)

    if ((min_next % 2) == 0 and sec_next == 0) and (min_next > min or min_next == 0):
        out.release()
        path_file = path + time.strftime("%Y%m%d-%H%M%S", localtime) + '.mp4'
        min = localtime.tm_min
        out = cv2.VideoWriter(path_file, fourcc, record_fps, (width, height))
    if not(r_f ==3 or r_f ==5 or r_f ==8 or r_f ==10 or r_f ==13 or r_f ==15 or r_f ==18 or r_f ==20 or r_f ==23 or r_f == 25):
        out.write(img)
    else:
        img=cv2.resize(img, (int(width*0.8), int(height*0.8)), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('Streaming', img)

    if r_f >= 25:
        r_f = 1
    else:
        r_f = r_f + 1

    key = cv2.waitKey(22)   # (int(1/record_fps*1000))
    if (key & 0xFF) == 27:
        out.release()
        cv2.destroyAllWindows()
        cam.stop()
        break
