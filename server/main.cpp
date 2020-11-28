// #include"tcp_pthread_server.hpp"
// #include<string>
// using namespace std;

// void HttpProcess(string& req, string* resp)
// {
//     printf("request: %s\n",req);
//     string first_line = "HTTP/1.0 200 OK\n";

//     // string body = "<html lang=\"zh-cn\">\
//     //             <!测试 test>\
//     //             <body bgcolor=\"White\">\
//     //             <div>\
//     //             <br/>\
//     //             <h1 align=\"center\">hehe</h1>\
//     //             <hr/>\
//     //             <br/>\
//     //             <p style = \"background-color:Red\">Hello World</p>\
//     //             <hr/>\
//     //             <p style = \"front-family:arial;color:yellow;front-size:20px;\">HAHA.</p>\
//     //             <a href=\"http://ww.w3school.com.cn\">w3school</a>\
//     //             </div>\
//     //             <img src=http://192.168.43.77:8080/?action=stream />\
//     //             <img src=\"ori.jpg\" />\
//     //             </body>\
//     //             </html>\n";
//     // string header = "Content-Type: text/html\ncharset: gbk\nContent-Length:"
//     //         +to_string(body.size())+"\n\n";
//     string body = "hello";
//     string header = "Content-Type: text/plain\ncharset: gbk\nContent-Length:"
//             +to_string(body.size())+"\n\n";
//     *resp = first_line + header + body;
// }
// int main()
// {
//   TcpPthreadServer server("0.0.0.0",9090);
//   server.Start(HttpProcess);
//   return 0;
// }

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>


int main()
{
  
  int sock_fd = socket(AF_INET, SOCK_DGRAM, 0);
  if(sock_fd < 0)
  {
    perror("socket");
    exit(1);
  }

  
  struct sockaddr_in addr_serv,addr_client;
  int len;
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


  int recv_num;
  int send_num;
  char send_buf[20] = "i am server!";
  char recv_buf[20];

  while(1)
  {
    printf("server wait:\n");

    recv_num = recvfrom(sock_fd, recv_buf, sizeof(recv_buf), 0, (struct sockaddr *)&addr_client, (socklen_t *)&len);

    if(recv_num < 0)
    {
      perror("recvfrom error:");
      exit(1);
    }

    recv_buf[recv_num] = '\0';
    printf("server receive %d bytes: %s\n", recv_num, recv_buf);

    send_num = sendto(sock_fd, send_buf, recv_num, 0, (struct sockaddr *)&addr_client, len);

    if(send_num < 0)
    {
      perror("sendto error:");
      exit(1);
    }
  }

  close(sock_fd);

  return 0;
}
