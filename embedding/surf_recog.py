import cv2,csv
import numpy as np

splitted_path='./splitted_pic/'

if __name__ == '__main__':
    img_sample = cv2.imread('./6.jpg')        # 读取样本图片
    img_sample=cv2.resize(img_sample, (0, 0), fx=0.25, fy=0.25)
    # img2 = cv2.imread('./ori.jpg')
    img_sources=[]

    # 参数为hessian矩阵的阈值
    surf_sample = cv2.xfeatures2d.SURF_create(5000)
    surf_source = cv2.xfeatures2d.SURF_create(5000)

    with open(splitted_path+'splitted_base.csv','r') as f:  # 读取分割后的原图，并离线预处理
        lines = csv.reader(f)
        for item in lines:
            img_name = item[0]
            img = cv2.imread(splitted_path + img_name, cv2.IMREAD_COLOR)
            kp, des = surf_source.detectAndCompute(img, None)
            img_sources.append([img,eval(item[1]),eval(item[2]),kp,des])    # 储存：[原图, 纵坐标, 横坐标, 关键点, 描述符]


    # 计算样本图的关键点和描述符
    kp_sample, des_sample = surf_sample.detectAndCompute(img_sample, None)

    # 把特征点标记到图片上
    # img = cv2.drawKeypoints(img_sample, kp_sample, None)
    # cv2.imshow('sp', img)
    # cv2.waitKey(0)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    max_good_num=0
    best_matches=None
    best_img_source=None
    for img_source_item in img_sources:
        matches = flann.knnMatch(des_sample, img_source_item[4], k=2)

        good=[]
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.8*n.distance:
                good.append([m])
        if len(good)>=max_good_num:
            max_good_num=len(good)
            best_matches=good
            best_img_source=img_source_item

    img3 = cv2.drawMatchesKnn(img_sample, kp_sample, best_img_source[0], best_img_source[3], best_matches, None, flags=2)

    cv2.imshow('sp', img3)
    cv2.waitKey(0)