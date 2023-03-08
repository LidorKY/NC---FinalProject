import os.path
import pickle
from socket import *
from time import sleep
import socket
from scapy.all import *
import numpy

# ------Magic Numbers-------#
proxy_sport = 8080
proxy_ip = '127.0.0.1'
proxy_address = (proxy_ip, proxy_sport)

server_site_sport = 80
server_site = '127.0.0.1'
server_site_address = (server_site, server_site_sport)

server_objects_sport = 7104
server_objects = '127.0.0.1'
server_objects_address = (server_objects, server_objects_sport)
# --------------------------#


if __name__ == "__main__":
    print("hello I am the App server")
    proxy_main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_main_socket.bind(proxy_address)
    proxy_main_socket.listen(5)
    print("I am ready to get requests")

    print("waiting for accept")
    communicating_with_client, client_address = proxy_main_socket.accept()
    http_request = communicating_with_client.recv(8192)
    print("I have got the clients http request")

    print("start communcation with the first server")
    proxy_to_site_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_to_site_server.connect(server_site_address)
    proxy_to_site_server.send(http_request)
    print("the proxy sent http request to get the site")

    http_response = proxy_to_site_server.recv(8192)
    print("got http response")

    proxy_to_site_server.close()
    print("closed socket that connects with site server")
    #---------------------------------------#


    communicating_with_client.send(http_response)
    print("sent the site to the client")

    communicating_with_client.close()
    print("closed connection with client")



    while True:
        #----requesting objects----#
        communicating_with_client1, client_address1 = proxy_main_socket.accept()
        http_request = communicating_with_client1.recv(8192)
        print("I have got the clients http request")
        #----requesting objects----#


        # ---- communicating with objects server----#
        print("start communcation with the first server")

        proxy_to_site_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_to_site_server.connect(server_objects_address)
        proxy_to_site_server.send(http_request)
        print("the proxy sent http request to get the site")

        http_response = proxy_to_site_server.recv(8192).decode("utf-8")
        print("got http response")

        proxy_to_site_server.close()
        print("closed socket that connects with site server")
        # ---------------------------------------#

        if "image1.jpg" in http_response:
            print("the object is: image1.jpg")
            temp = "image1.jpg"
        elif "image2.jpeg" in http_response:
            print("the object is: image2.jpeg")
            temp = "image2.jpeg"
        elif "image3.jpeg" in http_response:
            print("the object is: image3.jpeg")
            temp = "image3.jpeg"
        else:
            print("error")
            temp = "error"
            break

        size = os.path.getsize(temp)
        print("the size = " + str(size))
        size_to_send = size.to_bytes(32, 'big')
        communicating_with_client1.send(size_to_send)


        fp = open(temp, "rb")
        image_to_send = fp.read()
        fp.close()

        #----sending the object back to the client----#
        communicating_with_client1.send(image_to_send)
        sleep(1)
        communicating_with_client1.send(http_response.encode())
        communicating_with_client1.close()
        #----sending the object back to the client----#











        # break
    proxy_main_socket.close()
    print("finish")



























