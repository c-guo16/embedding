import cv2
import numpy as np

img1 = cv2.imread('./5.jpg')
img2 = cv2.imread('./ori.jpg')

# 参数为hessian矩阵的阈值
surf = cv2.xfeatures2d.SURF_create(2000)
# 找到关键点和描述符
# find the keypoints and descriptors with SIFT
kp1, des1 = surf.detectAndCompute(img1,None)
kp2, des2 = surf.detectAndCompute(img2,None)
# 把特征点标记到图片上
# img = cv2.drawKeypoints(img1, kp1, None)
# cv2.imshow('sp', img)
# cv2.waitKey(0)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

good=[]
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.8*n.distance:
        good.append([m,n])

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 2)

img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)

cv2.imshow('sp', img3)
cv2.waitKey(0)