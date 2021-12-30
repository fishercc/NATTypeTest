# -*- coding: utf-8 -*-

import socket  # 导入socket模块
import time  # 导入time模块

# server 接收端
def lisenUdp1():
    # 创建一个套接字socket对象，用于进行通讯
    # socket.AF_INET 指明使用INET地址集，进行网间通讯
    # socket.SOCK_DGRAM 指明使用数据协议，即使用传输层的udp协议
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP_PORT1 = ("0.0.0.0", 服务器端口1)
    server_socket.bind(IP_PORT1)  # 为服务器绑定一个固定的地址，ip和端口
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP_PORT2 = ("0.0.0.0", 服务器端口2)
    server_socket2.bind(IP_PORT2)  # 为服务器绑定一个固定的地址，ip和端口
    print('lisenUdp1 run ', IP_PORT1)
    #server_socket.settimeout(100)  # 设置一个时间提示，如果10秒钟没接到数据进行提示
    while True:
        # 正常情况下接收数据并且显示，如果10秒钟没有接收数据进行提示（打印 "time out"）
        # 当然可以不要这个提示，那样的话把"try:" 以及 "except"后的语句删掉就可以了
        try:
            # 接收客户端传来的数据 recvfrom接收客户端的数据，默认是阻塞的，直到有客户端传来数据
            # recvfrom 参数的意义，表示最大能接收多少数据，单位是字节
            # recvfrom返回值说明
            # receive_data表示接受到的传来的数据,是bytes类型
            # client  表示传来数据的客户端的身份信息，客户端的ip和端口，元组
            print("recvfrom !")
            receive_data, client = server_socket.recvfrom(1024)

            #now = time.time()  # 获取当前时间
            revMSG =receive_data.decode("utf-8")
            print("来自%s,发送的%s" % (client, revMSG))  # 打印接收的内容
            if revMSG == 'A': #向服务器的(IP-1,Port-1)发送数据包要求服务器返回客户端（NAT）的IP和Port
                msg = "%s" % (client,)  # ip port
                server_socket.sendto(msg.encode('utf-8'), client)  # （NAT）的IP和Port
            if revMSG == 'B':  #向服务器的(IP-1,Port-1)发送数据包要求服务器用另一对(IP-2,Port-2)响应客户端的请求往回发
                msg = "C#%s" % (client,)  # ip port
                server_socket.sendto(msg.encode('utf-8'), IP_PORT2)  # （NAT）的IP和Port
            if revMSG == 'D': #
                msg = "%s" % (client,)  # ip port
                server_socket.sendto(msg.encode('utf-8'), client)  # （NAT）的IP和Port
            if revMSG == 'E': #
                msg = "%s" % (client,)  # ip port
                server_socket2.sendto(msg.encode('utf-8'), client)  # （NAT）的IP和Port

            #print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))  # 以指定格式显示时间


        except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
            print("time out")

def lisenUdp2():
    # 创建一个套接字socket对象，用于进行通讯
    # socket.AF_INET 指明使用INET地址集，进行网间通讯
    # socket.SOCK_DGRAM 指明使用数据协议，即使用传输层的udp协议
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP_PORT2 = ("0.0.0.0", 10001)
    server_socket.bind(IP_PORT2)  # 为服务器绑定一个固定的地址，ip和端口
    #server_socket.settimeout(100)  # 设置一个时间提示，如果10秒钟没接到数据进行提示
    print('lisenUdp1 run ', IP_PORT2)
    while True:
        # 正常情况下接收数据并且显示，如果10秒钟没有接收数据进行提示（打印 "time out"）
        # 当然可以不要这个提示，那样的话把"try:" 以及 "except"后的语句删掉就可以了
        try:
            print("recvfrom !")
            receive_data, client = server_socket.recvfrom(1024)
            revMSG = receive_data.decode("utf-8")
            msglist = revMSG.split("#", 1)
            print("来自%s,发送的%s" % (client, revMSG))  # 打印接收的内容
            if msglist[0] == 'C':  #(IP-2,Port-2)响应客户端的请求往回发
                NatIP = tuple(eval(msglist[1]))
                server_socket.sendto(msglist[1].encode('utf-8'), NatIP)  # （NAT）的IP和Port
            if msglist[0] == 'D': #
                    msg = "%s" % (client,)  # ip port
                    server_socket.sendto(msg.encode('utf-8'), client)  # （NAT）的IP和Port

        except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
            print("time out")



if __name__ == '__main__':
    msg = input("input select 1 or 2:")
    if msg == '1':
        lisenUdp1()
    if msg == '2':
        lisenUdp2()
    print('run over')


