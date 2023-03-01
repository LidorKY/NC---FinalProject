
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
            data = data.encode("utf-8")
            client.sendto(data, ("192.168.1.1", 20230))

            print("---The client has successfully diconected from the server")
            break

        # encoding the data
        data = data.encode()

        # send the data to the server
        client.sendto(data, ("192.168.1.1", 20230))
        print("sent request to proxy")






        #we want to get ack from the proxy
        data, addr = client.recvfrom(1024)

        if data.decode("utf-8") != 'ack':
            print("error")
            break

        else:
            print("got ack")



        # we want to get the site from the proxy
        data, addr = client.recvfrom(1024)

        if data.decode("utf-8") != 'example.com':
            print("error")
            break

        else:
            print("example.com")

        # send ack
        data = data.encode("utf-8")
        client.sendto(data, ("192.168.1.1", 1030))











        # receiving data from the server
        data, addr = client.recvfrom(1024)

        # decoding tha data
        data = data.decode("utf-8")

        # print the data we have got from the server
        print("The new data: ", data)
        print("\n")

    # close the socket
    client.close()
    print("---Successfully closed the socket")


