import threading,time,random,json,socket
import struct

from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn


# orig_img = cv2.imread("1.jpg", cv2.IMREAD_GRAYSCALE)
# show_img = orig_img.copy()
# http server handler


def byte2float(x):
    return struct.unpack('<f', x)[0]

#创建socket对象
#SOCK_DGRAM  udp模式
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 11112))
datas={
    "x1":33,
    "x2":33,
    "x3":33,
    "x4":33,
    "y1":33,
    "y2":33,
    "y3":33,
    "y4":33,
    "xcenter":33,
    "ycenter":33,
    "fps":33
}

class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        global show_img
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()

            img_str = open("1.jpg",'rb').read()
            self.wfile.write("--jpgboundary".encode('utf-8'))
            self.send_header('Content-type','image/jpeg')
            self.send_header('Content-length',len(img_str))
            self.end_headers()
            self.wfile.write(img_str)

        if self.path.endswith('text'):
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(datas).encode('utf-8'))

        if self.path == '/':
            self.path = "index.html"
            super().do_GET()

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def server_start():
    server = ThreadingHTTPServer(('0.0.0.0', 9090), MyHandler)
    print("running...")
    server.serve_forever()

# run server in another thread
server_t = threading.Thread(target=server_start)
server_t.setDaemon(True)
server_t.start()

while True:
    data, addr = s.recvfrom(1024)
    print("recv: ")
    print(data[0:4])
    print(byte2float(data[0:4]))
    datas["x1"]=byte2float(data[0:4])
    datas["x2"]=byte2float(data[4:8])
    datas["x3"]=byte2float(data[8:12])
    datas["x4"]=byte2float(data[12:16])
    datas["y1"]=byte2float(data[16:20])
    datas["y2"]=byte2float(data[20:24])
    datas["y3"]=byte2float(data[24:28])
    datas["y4"]=byte2float(data[28:32])
    datas["xcenter"]=byte2float(data[32:36])
    datas["ycenter"]=byte2float(data[36:40])
    datas["fps"]=int(data[40])
