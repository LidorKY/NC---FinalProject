import os.path
from time import sleep
import socket
from scapy.all import *

# ------Magic Numbers-------#
proxy_sport = 8080
proxy_ip = '127.0.0.1'
proxy_address = (proxy_ip, proxy_sport)

server_site_sport = 80
server_site_ip = '127.0.0.1'
server_site_address = (server_site_ip, server_site_sport)

server_objects_sport = 7104
server_objects_ip = '127.0.0.1'
server_objects_address = (server_objects_ip, server_objects_sport)
# --------------------------#


if __name__ == "__main__":
    #----open the main server socket----#
    print("hello I am the App server")
    proxy_main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_main_socket.bind(proxy_address)
    proxy_main_socket.listen(5)
    print("I am ready to get requests")
    #-----------------------------------#


    #----receiving client's request for site----#
    print("waiting for accept")
    communicating_with_client, client_address = proxy_main_socket.accept()
    http_request = communicating_with_client.recv(8192)
    print("I have got the clients http request")
    #-------------------------------------------#


    #----communicating with the server that has the site----#
    print("start communcation with the first server")
    proxy_to_site_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_to_site_server.connect(server_site_address)
    proxy_to_site_server.send(http_request)
    print("the proxy sent http request to get the site")
    http_response = proxy_to_site_server.recv(8192)
    print("got http response")
    proxy_to_site_server.close()
    print("closed socket that connects with site server")
    #-------------------------------------------------------#


    #----sending the site to the client----"
    communicating_with_client.send(http_response)
    print("sent the site to the client")
    communicating_with_client.close()
    print("closed connection with client")
    #----sending the site to the client----"


    # ----loop for requesting objects----#
    while True:
        #----communicating with client to give him objects from the site----#
        communicating_with_client1, client_address1 = proxy_main_socket.accept()
        http_request = communicating_with_client1.recv(8192)
        print("I have got the clients http request")


        # ---- communicating with objects server----#
        print("start communcation with the object's server")
        proxy_to_site_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_to_site_server.connect(server_objects_address)
        proxy_to_site_server.send(http_request)
        print("the proxy sent http request to get the object")
        http_response = proxy_to_site_server.recv(8192).decode("utf-8")
        print("got http response")
        proxy_to_site_server.close()
        print("closed socket that connects with object's server")
        # ------------------------------------------#

        if "image1.jpg" in http_response:
            print("the object is: image1.jpg")
            temp = "image1.jpg"
        elif "image2.jpg" in http_response:
            print("the object is: image2.jpg")
            temp = "image2.jpg"
        elif "image3.jpg" in http_response:
            print("the object is: image3.jpg")
            temp = "image3.jpg"
        else:
            print("error")
            temp = "error"
            break

        #----sending file's size----#
        size = os.path.getsize(temp)
        print("the size = " + str(size))
        size_to_send = size.to_bytes(32, 'big')
        communicating_with_client1.send(size_to_send)
        #---------------------------#


        #----sending the object back to the client----#
        fp = open(temp, "rb")
        image_to_send = fp.read()
        fp.close()
        communicating_with_client1.send(image_to_send)
        print("the object has been sent successfully. ")
        sleep(3)
        communicating_with_client1.send(http_response.encode())
        communicating_with_client1.close()
        #----sending the object back to the client----#


    proxy_main_socket.close()
    print("finish")
