import os.path
import pickle
from socket import *
from time import sleep

from scapy.all import *
import numpy

# ------Magic Numbers-------#
proxy_sport = 8080
proxy_ip = '127.0.0.1'
proxy_address = (proxy_ip, proxy_sport)

server_site_sport = 80
server_site = '127.0.0.1'
server_site_address = (server_site, server_site_sport)

server_files_sport = 80 #need to change
server_files = '127.0.0.1'
# --------------------------#


if __name__ == "__main__":
    print("hello I am the App server")
    proxy_main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_main_socket.bind(proxy_address)
    proxy_main_socket.listen(5)
    print("I am ready to get requests")

    while True:
        print("waiting for accept")
        communicating_with_client, client_address = proxy_main_socket.accept()
        http_request = communicating_with_client.recv(8192)
        print("I have got the clients http request")




        #---- communicating with site server----#
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
        print("try")










        # break
    proxy_main_socket.close()
    print("finish")



























