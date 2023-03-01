
from random import randint
import socket
from time import sleep

from socket import *
import requests
from numpy import character
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.l2 import Ether, ARP

server_site = '192.168.2.2'

def syn_packet():
    ip = IP()
    ip.src = "192.168.1.1"
    ip.dst = "192.168.2.2"

    tcp = TCP()
    tcp.sport = 1030
    tcp.dport = 80
    tcp.flags = "S"

    syn_packet = ip / tcp

    send(syn_packet)


def http_request():
    ip = IP()
    ip.src = "192.168.1.1"
    ip.dst = "192.168.2.2"

    tcp = TCP()
    tcp.sport = 1030
    tcp.dport = 80
    tcp.flags = "A"

    http = "GET /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n"

    http_request = ip / tcp / http

    send(http_request)



if __name__ == "__main__":

    # using UDP protocol
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # local host and port
    server.bind(("0.0.0.0", 20230))

    # the loop for receiving and sending the data
    print("hello I am the Proxy server - the actual app\n")
    while True:
        # receiving data
        data, address = server.recvfrom(1024)
        print("got message from client")

        # decoding tha data
        data = data.decode("utf-8")

        if data == "stop":
            print("Client has been successfully disconnected")
            break

        # print for check
        print("The data: ", data)

        #ack
        data = 'ack'

        # encoding the data
        data = data.encode()

        # send the ack back to the client
        server.sendto(data, address)
        ptint("sent ack to client")



        #want to go to server that holds the site - now tcp connection


        # Send the TCP SYN packet
        print("connecing to site server")
        sleep(2)
        syn_packet()

        syn_ack_packet = sniff(count=1, filter='tcp port 1030')

        # Create the HTTP GET request packet
        sleep(2)
        http_request()

        http_response = sniff(count=1, filter='tcp port 1030')

        # Print the HTTP response
        print(http_response.show())
        print("finished with site server")




        print("start responding to client")
        #need to get the site from the http response packet
        data = 'example.com'

        # encoding the data
        data = data.encode()

        #send the site to the client
        server.sendto(data, address)

        # receiving ack
        data, address = server.recvfrom(1024)

        if data.decode("utf-8") != 'ack':
            print("error")
            break

        else:
            print("got ack")

        print("finish!!!")
        break





    #close the socket
    server.close()
    print("---Successfully closed the socket")
