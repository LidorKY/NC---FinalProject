
import socket
from random import randint
import socket
from time import sleep

from numpy import character
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.http import HTTP, HTTPRequest
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.l2 import Ether, ARP
import http3

proxy_ip = '192.168.1.1'


if __name__ == "__main__":
    # client_request_packet()

    # using UDP protocol
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # the loop for receiving and sending the data
    print("hello I am the client\n")
    while True:

        # receiving data from user
        data = input("pls enter a site you want to get: ")
        print("\n")

        #option for closing the socket
        if data == "stop":
            data = data.encode()
            client.sendto(data, ("127.0.0.1", 20230))
            client.close()
            print("---The client has successfully disconected from the server")
            break

        # encoding the data
        data = data.encode()

        # send the data to the server
        client.sendto(data, ("127.0.0.1", 20230))
        print("sent request to proxy")






        #we want to get ack from the proxy
        data, addr = client.recvfrom(1024)

        if data.decode("utf-8") != 'ack':
            print("error")
            break

        else:
            print("got ack - for requesting the site")



        # we want to get the site from the proxy
        html_file, addr = client.recvfrom(1024)

        fp = open("TheSite", "a")

        fp.write(html_file.decode("utf-8"))

        fp.close()

        print("get the site from the proxy - example.com\n")



        # send ack
        data = 'ack'
        data = data.encode()
        client.sendto(data, ("127.0.0.1", 20230))
        print("sent ack for getting the site\n")



    # close the socket
    client.close()
    print("---Successfully closed the socket")


