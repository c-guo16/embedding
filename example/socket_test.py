#不需要建立连接
import socket,time
import struct

def byte2float(x):
    return struct.unpack('<f', x)[0]

#创建socket对象
#SOCK_DGRAM  udp模式
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 11112))
datas={
    "x1":None,
    "x2":None,
    "x3":None,
    "x4":None,
    "y1":None,
    "y2":None,
    "y3":None,
    "y4":None,
    "fps":None
}
while True:
    data, addr = s.recvfrom(1024)
    print("recv: ")
    print(data[0:4])
    print(byte2float(data[0:4]))
    datas["x1"]=data[0:4]
    datas["x2"]=data[4:8]
    datas["x3"]=data[8:12]
    datas["x4"]=data[12:16]
    datas["y1"]=data[16:20]
    datas["y2"]=data[20:24]
    datas["y3"]=data[24:28]
    datas["y4"]=data[28:32]
    datas["fps"]=data[32]