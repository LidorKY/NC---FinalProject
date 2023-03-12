
import os.path
import pickle
from socket import *
from time import sleep

from scapy.all import *
import numpy

# ------Magic Numbers-------#
proxy_sport = 20230
proxy_ip = '127.0.0.1'
server_site_sport = 80
server_site = '127.0.0.1'
server_objects_sport = 7104
server_objects = '127.0.0.1'
# --------------------------#


def Connection_with_server_site(proxy_tcp_server):
    http_request = b"GET /index.html HTTP/1.1\r\nHost: site.html\r\n\r\n"
    proxy_tcp_server.sendall(http_request)
    print("sent http request")
    http_response = proxy_tcp_server.recv(8192)
    print("got http response")
    proxy_tcp_server.close()
    print("closed socket with the site server")
    return http_response



def get_ack(data1):
    if data1.decode("utf-8") != 'ack':
        print("error")
        return

    else:
        print("got ack - for receiving the html file")


def send_ack(address1):
    data = 'ack'
    data = data.encode()
    proxy_udp.sendto(data, address1)
    print("sent ack to client")




if __name__ == "__main__":
    print("hello I am the Proxy server - the actual app\n")
    print("connecting to client")
    # using UDP protocol
    proxy_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # local host and port
    proxy_udp.bind((proxy_ip, proxy_sport))


    # receiving request from client to get the site
    data, address = proxy_udp.recvfrom(8192)
    data = data.decode("utf-8")
    print("got message from client - requesting the site")

    #send ack to client for the site request
    send_ack(address)

    # ######################################################################################################################

    # want to go to server that holds the site - now tcp connection
    print("connecting to site server")
    proxy_tcp_site = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_site_address = (server_site, server_site_sport)
    proxy_tcp_site.connect(server_site_address)
    resp = Connection_with_server_site(proxy_tcp_site)

    # #####################################################################################################################

    # send the site to the client
    print("sending site to client")
    proxy_udp.sendto(resp, address)

    # receiving ack
    data, address = proxy_udp.recvfrom(1024)
    get_ack(data)
    print("got ack from the client that he got the requested site")



    #----requesting objects from the objects server----#
    print("connecting to files server")
    proxy_tcp_files = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_files_address = (server_objects, server_objects_sport)
    proxy_tcp_files.connect(server_files_address)


    while True:
        # receiving which file the client wants
        data, address = proxy_udp.recvfrom(1024)
        data = data.decode("utf-8")
        print("got the request for object from the client")
        # need to send ack for getting request for a file
        send_ack(address)
        print("chosen object is " + data)

        if data == "image1.jpg":
            image = b"GET /index.jpg HTTP/1.1\r\nHost: image1.jpg\r\n\r\n"
        elif data == "image2.jpg":
            image = b"GET /index.jpeg HTTP/1.1\r\nHost: image2.jpg\r\n\r\n"
        elif data == "image3.jpg":
            image = b"GET /index.jpeg HTTP/1.1\r\nHost: image3.jpg\r\n\r\n"
        else:
            image = None
            print("error")
            print("somehow im here")
            break

        proxy_tcp_files.send(image)
        http_response = proxy_tcp_files.recv(8192).decode("utf-8")


        print("sending " + data + " to client")
        size = os.path.getsize(data)
        temp = size.to_bytes(32, 'big')
        proxy_udp.sendto(temp, address)  # sending the size of file
        print("sent the size of the object to the client")

        answer, address = proxy_udp.recvfrom(8192)
        get_ack(answer)
        print("received ack for sending the object size")

        # ----sending the object back to the client----#
        fp = open(data, "rb")
        current_size = 0
        while current_size < size:
            image_to_send = fp.read(8192)
            current_size = current_size + len(image_to_send)
            sleep(1)
            proxy_udp.sendto(image_to_send, address)
        fp.close()

        print("the object has been sent successfully. ")
        answer1, address = proxy_udp.recvfrom(8192)
        get_ack(answer1)
        print("received ack for sending the object")
        # ---------------------------------------------#













#     fp = open(file, "r")
#
#     packets_amount = int(size / 1024) + 1
#     packets = []
#     for i in range(0, packets_amount):  # splitting the file into packet size chunks
#         chunk_of_file = fp.read(1024)
#         tmp = str(i+1) + "$" + chunk_of_file
#         packets.append(tmp)
#
#     index = 0
#     window_size = 1
#     current_ack = 1
#     suppose_to_ack = 1
#     tmp = 0
#     proxy_udp.settimeout(5)
#     while index < packets_amount:  # The CC
#         tmp = 0
#         while window_size > tmp and index < packets_amount:
#             print("window size in sending" + str(window_size))
#             packets[index] = str(window_size) + "&" + packets[index]
#             to_send = packets[index].encode()
#             index += 1
#             sleep(1)
#             proxy_udp.sendto(to_send, address)
#             suppose_to_ack += 1
#             tmp += 1
#
#         tmp = 0
#         while window_size > tmp and index < packets_amount:
#             ack_sequence, address = proxy_udp.recvfrom(1024)
#             ack_sequence = ack_sequence.decode("utf-8")
#             print(current_ack)
#             print(ack_sequence[len(ack_sequence) - 1:len(ack_sequence)])
#             print(current_ack != int(ack_sequence[len(ack_sequence) - 1:len(ack_sequence)]))
#             if current_ack != int(ack_sequence[len(ack_sequence) - 1:len(ack_sequence)]):
#                 tmp += 1
#                 print("here2")
#                 continue
#             else:
#                 tmp += 1
#                 current_ack += 1
#                 print("increased temp" + str(tmp))
#                 print("innn else")
#
#             tmp += 1
#             print("increased temp " + str(tmp))
#
#
#         if suppose_to_ack != current_ack:
#             window_size = 1
#             index = current_ack
#
#         else:
#
#             window_size *= 2
#             index = current_ack
#             print("increased window size  " + str(window_size))
#
#
# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#     proxy_udp.settimeout(None)
#     print("finish " + counter.__str__() + " task")

    # close the socket
    proxy_udp.close()
    print("---Successfully closed the socket")