import cv2,numpy,csv

# num_of_res_needed=10000   #生成的训练图片的数量（大约）
# network_input_width=36
#
# if __name__ == '__main__':
#
#     img=cv2.imread("./1.jpg",cv2.IMREAD_COLOR)
#
#     img_width=img.shape[1]
#     img_height=img.shape[0]
#     lens_width=int(img_width/10)
#     scanned_width=img_width-lens_width
#     scanned_height=img_height-lens_width
#
#     aspect_ratio=scanned_width/scanned_height
#     height_square=num_of_res_needed/aspect_ratio
#     height_num=int(height_square**0.5)
#     width_num=int(num_of_res_needed/height_num)
#     stride=scanned_height/height_num
#
#     csv_contents=[]
#     for i in range(0,height_num):
#         for j in range(0,width_num):
#             pix_h=int(i*stride)
#             pix_w=int(j*stride)
#             res_img=img[pix_h:pix_h+lens_width,pix_w:pix_w+lens_width,:]
#             res_img=cv2.resize(res_img,(network_input_width,network_input_width))
#             fname="{0}_{1}.bmp".format(i,j)
#             cv2.imwrite("./res/"+fname,res_img)
#             csv_contents.append([fname,pix_h/img_height,pix_w/img_width])
#
#     with open('label.csv','w',newline='')as f:
#         f_csv = csv.writer(f)
#         f_csv.writerows(csv_contents)
#
#     cv2.imshow("sss",img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     cv2.destroyWindow("sss")

vertical_split_num=6
horizontal_split_num=8

if __name__ == '__main__':

    img=cv2.imread("./ori.jpg",cv2.IMREAD_COLOR)

    img_width=img.shape[1]
    img_height=img.shape[0]
    stride_height=img_height/vertical_split_num
    stride_width=img_width/horizontal_split_num

    csv_contents=[]
    posh=0
    posw=0
    for i in range(0,vertical_split_num-1):
        for j in range(0,horizontal_split_num-1):
            res_img=img[int(i*stride_height):int((i+2)*stride_height),int(j*stride_width):int((j+2)*stride_width),:]
            fname="{0}_{1}.bmp".format(i,j)
            cv2.imwrite("C:\Projects\Visual_Studio_2019\Projects\embedding\embedding\splitted_pic/"+fname,res_img)
            csv_contents.append([fname,i*stride_height/img_height,j*stride_width/img_width])

    # with open('./splitted_pic/splitted_base.csv','w',newline='')as f:
    #     f_csv = csv.writer(f)
    #     f_csv.writerows(csv_contents)

    with open('C:\Projects\Visual_Studio_2019\Projects\embedding\embedding\splitted_pic/splitted_base.txt','w')as f:
        f.write(str(img_height)+' '+str(img_width)+'\n')
        for item in csv_contents:
            f.write(item[0]+' '+str(item[1])+' '+str(item[2])+'\n')