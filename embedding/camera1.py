# -*- coding: utf-8 -*-
 
import cv2
 
cap = cv2.VideoCapture(0)          # 打开摄像头
print("VideoCapture is opened?", cap.isOpened())

photonum=0;

while(True):
 
 ret, frame = cap.read()          # 读取摄像头图像
 frame=frame[50:-50,50:-50]
 center = (frame.shape[1]//2, frame.shape[0]//2)    # 图像中心点位置
 
 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # 转灰度
 cv2.circle(gray, center=center, radius=100, color=(0,0,255)) # 画圆
 cv2.imshow("frame", frame)         # 显示图片
 
 key=cv2.waitKey(1)
 if key & 0xFF == ord('q'):
  break
 elif key & 0xFF == ord('w'):
  cv2.imwrite("{}.jpg".format(photonum),frame)
  photonum+=1
 
cap.release()   # 释放摄像头
cv2.destroyAllWindows() # 关闭所有窗口