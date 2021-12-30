# -*- coding: utf-8 -*-
import socket
import time
import threading

#client 发送端


IP1 = "本地IP"
PORT1 = 8000
server_IP1 = "公网服务器IP1"
server_PORT1 = 公网服务器端口1
server_IP2 =  "公网服务器IP2"
server_PORT2 = 公网服务器端口2

sendaddress = (IP1, PORT1)
#https://blog.csdn.net/a5243512/article/details/76577598?spm=1001.2101.3001.6650.7&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-7.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-7.no_search_link&utm_relevant_index=13
def th1(id, name):
      print(id+':线程开始运行...')


def th2(id, name):
      print(id+':线程开始运行...')


def NATTest():
      print('NAT test start...')
      nattype = 'IP Restricted Cone NAT'
      client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      client_socket.bind(sendaddress)  # 为服务器绑定一个固定的地址，ip和端口
      #第一步：检测客户端是否有能力进行UDP通信以及客户端是否位于NAT后？
      print('第一步：检测客户端是否有能力进行UDP通信以及客户端是否位于NAT后？')
      Count =0 #重复5次
      while Count<5:
            try:
                  server_address1 = (server_IP1, server_PORT1)  # 接收方 服务器的ip地址和端口号
                  msg = 'A' ##向服务器的(IP-1,Port-1)发送数据包要求服务器返回客户端（NAT）的IP和Port
                  client_socket.settimeout(0.5) #300ms
                  client_socket.sendto(msg.encode('utf-8'), server_address1) #将msg内容发送给指定接收方
                  receive_data, client = client_socket.recvfrom(1024)
                  revMSG =receive_data.decode("utf-8")
                  print("来自%s,发送的%s\n" % (client, revMSG))  # 打印接收的内容
                  sendipstr = "%s" % (sendaddress,)
                  if revMSG == sendipstr:
                        return '不存在NAT'
                  else:
                        break
            except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
                  Count = Count+1
                  print("time out:Count=", Count)
                  time.sleep(2) #2s
      if(Count >= 5):
            return '防火墙或NAT阻止UDP通信'

      print('继续检测 第二步：检测客户端NAT是否是Full Cone NAT？')
      #第二步：检测客户端NAT是否是Full Cone NAT？
      Count = 0  # 重复5次
      while Count < 5:
            try:
                  server_address1 = (server_IP1, server_PORT1)  # 接收方 服务器的ip地址和端口号
                  msg = 'B'  #向服务器的(IP-1,Port-1)发送数据包要求服务器用另一对(IP-2,Port-2)响应客户端的请求往回发
                  client_socket.settimeout(0.5)  # 300ms
                  client_socket.sendto(msg.encode('utf-8'), server_address1)  # 将msg内容发送给指定接收方
                  receive_data, client = client_socket.recvfrom(1024)
                  revMSG = receive_data.decode("utf-8")
                  print("来自%s,发送的%s\n" % (client, revMSG))  # 打印接收的内容
                  if revMSG != '':
                        return 'NAT1:Full Cone NAT'
                  else:
                        break

            except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
                  Count = Count + 1
                  print("time out:Count=", Count)
                  time.sleep(2)  # 2s
      if (Count >= 5):
            print('继续检测 第三步：检测客户端NAT是否是Symmetric NAT？')
      #第三步：检测客户端NAT是否是Symmetric NAT？
      '''
      threads = []
      t1 = threading.Thread(target=th1, args=(str(1), 'sento1'))
      t2 = threading.Thread(target=th2, args=(str(2), 'sento2'))
      threads.append(t1)
      t1.start()
      threads.append(t2)
      t2.start()
      print('主程序运行中...')
      # 等待所有线程任务结束。
      for t in threads:
            t.join()

      print("所有线程任务完成")
      '''
      Count = 0  # 重复5次
      while True:
            try:
                  server_address1 = (server_IP1, server_PORT1)  # 接收方 服务器的ip地址和端口号
                  msg = 'D'  # 向服务器的(IP-1,Port-1)发送数据包要求服务器用另一对(IP-2,Port-2)响应客户端的请求往回发
                  client_socket.settimeout(None)  # 300ms
                  client_socket.sendto(msg.encode('utf-8'), server_address1)  # 将msg内容发送给指定接收方
                  receive_data, client = client_socket.recvfrom(1024)
                  NATIP1 = receive_data.decode("utf-8")
                  print("来自%s,发送的%s\n" % (client, NATIP1))  # 打印接收的内容
                  server_address2 = (server_IP2, server_PORT2)  # 接收方 服务器的ip地址和端口号
                  msg = 'D#'  # 向服务器2的(IP-1,Port-1)发送数据包要求服务器用另一对(IP-2,Port-2)响应客户端的请求往回发
                  client_socket.settimeout(None)  # 300ms
                  client_socket.sendto(msg.encode('utf-8'), server_address2)  # 将msg内容发送给指定接收方
                  receive_data, client = client_socket.recvfrom(1024)
                  NATIP2 = receive_data.decode("utf-8")
                  print("来自%s,发送的%s\n" % (client, NATIP2))  # 打印接收的内容
                  if NATIP1 != NATIP2:
                        return 'NAT4:Symmetric NAT'
                  else:
                        break
            except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
                  Count = Count + 1
                  print("time out:Count=", Count)
                  time.sleep(2)  # 2s

      print('继续检测 第四步：检测客户端NAT是否是Restricted Cone NAT还是Port Restricted Cone NAT？')
      #第四步：检测客户端NAT是否是Restricted Cone NAT还是Port Restricted Cone NAT？
      Count = 0  # 重复5次
      while Count < 5:
            try:
                  server_address1 = (server_IP1, server_PORT1)  # 接收方 服务器的ip地址和端口号
                  msg = 'E'  # 向服务器的(IP-1,Port-1)发送数据包要求服务器用另一对(IP-2,Port-2)响应客户端的请求往回发
                  client_socket.settimeout(0.5)  # 300ms
                  client_socket.sendto(msg.encode('utf-8'), server_address1)  # 将msg内容发送给指定接收方
                  receive_data, client = client_socket.recvfrom(1024)
                  revMSG = receive_data.decode("utf-8")
                  print("来自%s,发送的%s\n" % (client, revMSG))  # 打印接收的内容
                  if revMSG != '':
                        return 'NAT2:IP Restricted Cone NAT'
                  else:
                        break

            except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
                  Count = Count + 1
                  print("time out:Count=", Count)
                  time.sleep(2)  # 2s
      if (Count >= 5):
            return 'NAT3:Port Restricted Cone NAT'



if __name__ == '__main__':
      msg = NATTest()
      print(msg)
      print('检测完成')
