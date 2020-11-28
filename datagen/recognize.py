#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Charles Guo'

import tensorflow as tf
import numpy as np
import read_data
from generate import network_input_width

#读取之前训练的模型的路径、测试集路径以及csv结果文件的路径：
ModelPath=r'./save.ckpt'
TestDataPath=r'./testld.bmp'


#初始化权重和偏置项：
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)    #权重使用高斯分布初始化
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)             #偏置项使用常量初始化
    return tf.Variable(initial)

#卷积和池化：
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):    #使用2*2最大值池化
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1], padding='SAME')

#设置参数：
x = tf.placeholder("float", [None, network_input_width*network_input_width])
W = tf.Variable(tf.zeros([network_input_width*network_input_width,2]))
b = tf.Variable(tf.zeros([2]))
x_image = tf.reshape(x, [-1,network_input_width,network_input_width,1])

#输入层dropout：
keep_prob_input = tf.placeholder("float")
x_drop = tf.nn.dropout(x_image, keep_prob_input)

#第一层卷积，使用32个5*5卷积核，然后池化：
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_drop, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

#第二层卷积，使用1input_width个5*5卷积核，然后池化：
W_conv2 = weight_variable([5, 5, 32, 128])
b_conv2 = bias_variable([128])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

h_reshape2 = tf.reshape(h_pool2, [-1, 9 * 9 * 128])

#全连接层，有1024个节点：
W_fc1 = weight_variable([9 * 9 * 128, 1024])
b_fc1 = bias_variable([1024])
h_fc1 = tf.nn.relu(tf.matmul(h_reshape2, W_fc1) + b_fc1)

#全连接层dropout：
keep_prob_fc = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob_fc)

#输出层：
W_fc2 = weight_variable([1024, 2])
b_fc2 = bias_variable([2])
y_conv=tf.matmul(h_fc1_drop, W_fc2) + b_fc2

#计算损失：
y_ = tf.placeholder("float", [None,2])
loss = tf.losses.mean_squared_error(y_,y_conv)

#初始化变量并启动模型：
init = tf.global_variables_initializer()
sess = tf.InteractiveSession()
sess.run(init)

#加载训练好的模型参数：
saver = tf.train.Saver()
saver.restore(sess,ModelPath)

#加载测试集：
pictures=read_data.read_test_data(TestDataPath)

#进行测试：
prediction = y_conv
for i in range(pictures.shape[0]):
    predint=prediction.eval(feed_dict={x: [pictures[i].tolist()], keep_prob_fc: 1.0, keep_prob_input:1.0}, session=sess)
    print(predint)

#输出结果：
# np.savetxt(outPutPath,result,fmt="%d",delimiter=',')