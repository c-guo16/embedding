import numpy as np
import pandas as pd
import cv2,csv
from generate import num_of_res_needed

def read_train_data(filename,img_path):
    '''
    读取训练数据，返回N*(2+36^2)的矩阵，N为训练数据总数，前2个为标签，后36^2为图片
    '''
    data=[]
    with open(filename)as f:
        labels = csv.reader(f)
        for item in labels:
            img_name=item[0]
            img = cv2.imread(img_path+img_name, cv2.IMREAD_GRAYSCALE)
            img=img.flatten()
            img=np.hstack((np.array([item[1],item[2]]),img))
            data.append(list(map(eval,img.tolist())))
            for i in range(2,len(data[-1])):
                data[-1][i]/=255

    # dataSet = pd.read_csv(filename)
    # dataMat = np.array(dataSet)
    #
    # dataLabel = dataMat[:, 0]           #将训练数据集分离第一列为label
    # dataMat = dataMat[:, 1:]            #其它列为特征
    #
    # dLabel=np.zeros((dataMat.shape[0],2))
    # for i in range(dataMat.shape[0]):  #构造输入数据标签
    #     dLabel[i,dataLabel[i]]=1
    # #像素二值化，采用四舍五入：
    # dataMat=np.round(dataMat/255)
    # result=np.column_stack((dLabel,dataMat))
    return np.array(data)

def read_test_data(filename):
    '''
    读取测试数据，区别在于不需要数据标签
    '''
    data = []
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img = img.flatten()
    data.append(img.tolist())
    return np.array(data)/255