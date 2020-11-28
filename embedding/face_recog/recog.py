import cv2 as cv

cap = cv.VideoCapture(0)          # 打开摄像头
print("VideoCapture is opened?", cap.isOpened())

# Load the model 
net = cv.dnn.readNet('face-detection-adas-0001.xml', 'face-detection-adas-0001.bin') 
# Specify target device 
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

while(True):
 
 ret, frame = cap.read()          # 读取摄像头图像
 # Prepare input blob and perform an inference 
 blob = cv.dnn.blobFromImage(frame, size=(672, 384), ddepth=cv.CV_8U)
 net.setInput(blob) 
 out = net.forward()
 # Draw detected faces on the frame 
 for detection in out.reshape(-1, 7): 
  confidence = float(detection[2]) 
  xmin = int(detection[3] * frame.shape[1]) 
  ymin = int(detection[4] * frame.shape[0]) 
  xmax = int(detection[5] * frame.shape[1]) 
  ymax = int(detection[6] * frame.shape[0])
  if confidence > 0.5:
   cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0),thickness=3)
 cv.imshow("frame", frame)         # 显示图片
 
 if cv.waitKey(1) & 0xFF == ord('q'):
  break

cap.release()   # 释放摄像头
cv.destroyAllWindows() # 关闭所有窗口