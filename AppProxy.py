
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
    porxy_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # local host and port
    porxy_udp.bind(('', 20230))

    # the loop for receiving and sending the data
    print("hello I am the Proxy server - the actual app\n")
    while True:
        # receiving data
        data, address = porxy_udp.recvfrom(1024)
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
        porxy_udp.sendto(data, address)
        print("sent ack to client")

########################################################################################################################

        #want to go to server that holds the site - now tcp connection


        # # Send the TCP SYN packet
        # print("connecing to site server")
        # sleep(2)
        # syn_packet()
        # print("sent syn")
        #
        # syn_ack_packet = sniff(count=1, filter='tcp port 1030')
        # print("get syn ack")
        #
        #
        # # Create the HTTP GET request packet
        # sleep(2)
        # http_request()
        # print("sent http request")
        #
        # http_response = sniff(count=1, filter='tcp port 1030')
        #
        # # Print the HTTP response
        # http_response[0].show()
        # print("finished with site server")

        print("connecting to site server")
        proxy_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_site_address = ('127.0.0.1', 80)

        proxy_tcp.connect(server_site_address)

        http_request = b"GET /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n"

        proxy_tcp.sendall(http_request)
        print("sent http request")

        http_response = proxy_tcp.recv(1024)
        print("got http response")

        proxy_tcp.close()
        print("closed tcp socket")



######################################################################################################################
        print("start responding to client")
        fp = open("site.html", 'r')

        #need to get the site from the http response packet
        data = fp.read(-1)

        # encoding the data
        data = data.encode()

        #send the site to the client
        porxy_udp.sendto(data, address)

        # receiving ack
        data, address = porxy_udp.recvfrom(1024)

        if data.decode("utf-8") != 'ack':
            print("error")
            break

        else:
            print("got ack - for receiving the html file")

        print("finish!!!")
        break





    #close the socket
    porxy_udp.close()
    print("---Successfully closed the socket")
