#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/xfeatures2d.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include<sys/time.h>


using namespace std;
using namespace cv;
using namespace cv::xfeatures2d;

struct sockaddr_in addr_serv,addr_client;
int len,fps_cnt;
u_char fps=0;
struct timeval start;   //计算fps使用
struct timeval endd;
int sock_fd;
Mat frame; // 线程共享
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
void thread_read_cap(){
    VideoCapture capture(0);
    if(!capture.isOpened()){ 
        cout<<"fail to open!"<<endl;
        return;
    }   
    cout<<"captured!"<<endl;
    while(1){
        // pthread_mutex_lock(&mutex);
        capture.read(frame);
        // pthread_mutex_unlock(&mutex);
    }   
    capture.release();   

}

void init_socket(){
    sock_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if(sock_fd < 0)
    {
        perror("socket");
        exit(1);
    }
    memset(&addr_serv, 0, sizeof(struct sockaddr_in));
    addr_serv.sin_family = AF_INET;
    addr_serv.sin_port = htons(11111);
    addr_serv.sin_addr.s_addr = inet_addr("127.0.0.1");
    len = sizeof(addr_serv);
    memset(&addr_client, 0, sizeof(struct sockaddr_in));
    addr_client.sin_family = AF_INET;
    addr_client.sin_port = htons(11112);
    addr_client.sin_addr.s_addr = inet_addr("127.0.0.1");
    if(bind(sock_fd, (struct sockaddr *)&addr_serv, sizeof(addr_serv)) < 0)
    {
        perror("bind error:");
        exit(1);
    }

    gettimeofday(&start,NULL);
}

int main() {
    init_socket();

    pthread_t thread_read;
    if( 0!=pthread_create(&thread_read, NULL, (void *(*)(void *))thread_read_cap,NULL)){
        printf("pthread create failed!/n");
        return -1;
    }

	//VideoCapture cap(0);
    // if(!cap.open("http://192.168.43.77:8080/?action=stream")) {  //读取网络摄像头失败？？？
    //     cout << "Error opening video stream or file" << std::endl;
    //     return -1;
    // }
	//cout << "VideoCapture is opened?" << cap.isOpened();

	int photonum = 0;
	string splitted_path = "./splitted_pic/";
	string splitted_base = "splitted_base.txt";

	vector<Mat> img_sources0;
	vector<float> img_sources1;
	vector<float> img_sources2;
	vector<vector<KeyPoint>> img_sources3;
	vector<Mat> img_sources4;
	vector<FlannBasedMatcher> flann_matchers;

	//参数为hessian矩阵的阈值
	Ptr<SURF> surf_sample = SURF::create(5000);
	Ptr<SURF> surf_source = SURF::create(10000);

	string fname;
	float f1, f2;
	Mat img,img_ori;
	int ori_pic_rows, ori_pic_cols;
	img_ori = imread("./ori.jpg",IMREAD_GRAYSCALE);
	ifstream in(splitted_path + splitted_base);
	in >> ori_pic_rows >> ori_pic_cols;
	while (!in.eof()) {
		in >> fname >> f1 >> f2;
		img = imread(splitted_path+fname, IMREAD_GRAYSCALE);
		img_sources0.push_back(img);
		img_sources1.push_back(f1);
		img_sources2.push_back(f2);
		vector<KeyPoint> keypoints;
		Mat descriptors;
		surf_source->detectAndCompute(img, noArray(),keypoints,descriptors);
		img_sources3.push_back(keypoints);
		img_sources4.push_back(descriptors);
	}

	Mat tempMat;
	int notfound_cnt = 0;
	while (true) {

		//cap >> frame;
        //pthread_mutex_lock(&mutex);
		tempMat = frame(Rect(50, 50, frame.cols-100, frame.rows - 100));
        //pthread_mutex_unlock(&mutex);
		cvtColor(tempMat, tempMat, COLOR_BGR2GRAY, 1);
		resize(tempMat, tempMat, Size(), 0.25, 0.25);		//重要：调整图片大小！！
		
		//tempMat = imread("6.jpg");
		//imshow("camera", tempMat);

		vector<KeyPoint> keypoints_sample;
		Mat descriptors_sample;
		surf_sample->detectAndCompute(tempMat,Mat(), keypoints_sample, descriptors_sample);
		int max_good_num = 0,best_img_source=-1;
		vector<DMatch> best_good;
		for (size_t i = 0; i < img_sources0.size(); i++) {
			vector<vector<DMatch>> matches;
			FlannBasedMatcher flann;
			flann.knnMatch(descriptors_sample, img_sources4[i],matches,2);
			vector<DMatch> good;
			for (int j = 0; j < matches.size();j++) {
				if (matches[j][0].distance < 0.7 * matches[j][1].distance) {
					good.push_back(matches[j][0]);
				}
			}
			if (good.size() >= max_good_num) {
				max_good_num = good.size();
				best_good = good;
				best_img_source = i;
			}
		}
		//Mat res;
		//drawMatches(tempMat, keypoints_sample, img_sources0[best_img_source], img_sources3[best_img_source], best_good, res);
		
		//寻找匹配上的关键点的变换
		vector<Point2f> obj;  //目标特征点
		vector<Point2f> objInScene;  //场景中目标特征点
		for (size_t t = 0; t < best_good.size(); t++) {
			obj.push_back(keypoints_sample[best_good[t].queryIdx].pt);
			objInScene.push_back(img_sources3[best_img_source][best_good[t].trainIdx].pt);
		}
		if (obj.empty()) {
			cout << notfound_cnt++ << "无法找到图像（匹配特征点数量不足）！" << endl;
			continue;
		}
		Mat imgBH = findHomography(obj, objInScene, RANSAC,0,noArray(),4000,0.7);
		if (imgBH.empty()) {
			cout << notfound_cnt++ << "无法找到图像（找不到变换矩阵）！" << endl;
			continue;
		}

		//映射点
		vector<Point2f> obj_corners(4);
		vector<Point2f> scene_corners(4);
		obj_corners[0] = Point(0, 0);
		obj_corners[1] = Point(tempMat.cols, 0);
		obj_corners[2] = Point(tempMat.cols, tempMat.rows);
		obj_corners[3] = Point(0, tempMat.rows);
		perspectiveTransform(obj_corners, scene_corners, imgBH);

		scene_corners[0].x += img_sources2[best_img_source] * img_ori.cols;
		scene_corners[1].x += img_sources2[best_img_source] * img_ori.cols;
		scene_corners[2].x += img_sources2[best_img_source] * img_ori.cols;
		scene_corners[3].x += img_sources2[best_img_source] * img_ori.cols;
		scene_corners[0].y += img_sources1[best_img_source] * img_ori.rows;
		scene_corners[1].y += img_sources1[best_img_source] * img_ori.rows;
		scene_corners[2].y += img_sources1[best_img_source] * img_ori.rows;
		scene_corners[3].y += img_sources1[best_img_source] * img_ori.rows;
		float xcenter = (float)(scene_corners[0].x + scene_corners[1].x + scene_corners[2].x + scene_corners[3].x) / (4 * img_ori.cols);
		float ycenter = (float)(scene_corners[0].y + scene_corners[1].y + scene_corners[2].y + scene_corners[3].y) / (4 * img_ori.rows);
		cout << "(" << xcenter << "," << ycenter << ")" << endl;

        // 四个点之间画线
		// Mat dst = img_ori.clone();
		// line(dst, scene_corners[0], scene_corners[1], Scalar(0, 0, 255), 2, 8, 0);
		// line(dst, scene_corners[1], scene_corners[2], Scalar(0, 0, 255), 2, 8, 0);
		// line(dst, scene_corners[2], scene_corners[3], Scalar(0, 0, 255), 2, 8, 0);
		// line(dst, scene_corners[3], scene_corners[0], Scalar(0, 0, 255), 2, 8, 0);
		// resize(dst, dst, Size(), 0.5, 0.5);
		// imshow("frame", dst);

        float x1=(float)(scene_corners[0].x);
        float x2=(float)(scene_corners[1].x);
        float x3=(float)(scene_corners[2].x);
        float x4=(float)(scene_corners[3].x);
        float y1=(float)(scene_corners[0].y);
        float y2=(float)(scene_corners[1].y);
        float y3=(float)(scene_corners[2].y);
        float y4=(float)(scene_corners[3].y);
        fps_cnt++;
        gettimeofday(&endd,NULL);
        float time_use=(endd.tv_sec-start.tv_sec)+(endd.tv_usec-start.tv_usec)/1000000.0;
        if(time_use>3){
            printf("fps_cnt: %d\n",fps_cnt);
            fps=u_char(ceil(fps_cnt/time_use));
            gettimeofday(&start,NULL);
            fps_cnt=0;
        }
        // 发送匹配位置和fps信息：
        u_char send_buf[100];
        int send_num;
        memcpy(&(send_buf[0]),&x1,4);
        memcpy(&(send_buf[4]),&x2,4);
        memcpy(&(send_buf[8]),&x3,4);
        memcpy(&(send_buf[12]),&x4,4);
        memcpy(&(send_buf[16]),&y1,4);
        memcpy(&(send_buf[20]),&y2,4);
        memcpy(&(send_buf[24]),&y3,4);
        memcpy(&(send_buf[28]),&y4,4);
        memcpy(&(send_buf[32]),&xcenter,4);
        memcpy(&(send_buf[36]),&ycenter,4); 
        send_buf[40]=fps;     
        send_num = sendto(sock_fd, send_buf, 41, 0, (struct sockaddr *)&addr_client, len);
        if(send_num < 0){
            perror("sendto error:");
        }
		// waitKey(10);	//可控制帧率
	}
	return 0;
}

