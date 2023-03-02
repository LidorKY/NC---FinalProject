import socket
from datetime import date
from random import randint
import socket
from time import sleep
import time

from numpy import character
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.http import HTTPResponse, HTTP
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.l2 import Ether, ARP
import socket

def ack_packet(syn_packet):
    ip = IP()
    ip.src = syn_packet[0][IP].dst
    ip.dst = syn_packet[0][IP].src


    tcp = TCP()
    tcp.sport = syn_packet[0][TCP].dport
    tcp.dport = syn_packet[0][TCP].sport
    tcp.flags = "A" #check the flags

    ack_packet = ip / tcp

    send(ack_packet)



def resp_packet(req_packet):
    ip = IP()
    ip.src = req_packet[0][IP].dst
    ip.dst = req_packet[0][IP].src

    tcp = TCP()
    tcp.sport = req_packet[0][TCP].dport
    tcp.dport = req_packet[0][TCP].sport
    tcp.flags = "A"
    tcp.seq = 1000
    tcp.ack = 2000

    # html_page = """<html><body>.....blablabla....</body></html>"""

    http = HTTP()
    # http.Status_Code = 200
    # http.Reason = 'OK'
    # http.HTTP_Version = 'HTTP/1.1'
    # http.date = time.time()
    # http.Server = 'Site_Server'
    # http.Content_Type = 'text/html; \r\n\r\n' + html_page

    html_page = """<html><body>.....blablabla....</body></html>"""

    http = HTTP(b'HTTP/1.1 200 OK\r\nContent_Type: text/html\r\n\r\n <html><body>.....blablabla....</body></html>')

    response_packet = ip / tcp / http

    send(response_packet)



if __name__ == "__main__":
    # print("hello i am the site server")
    #
    # syn_pack = sniff(count=1, filter='tcp port 80')
    # print("got syn")
    #
    # sleep(2)
    # ack_packet(syn_pack)
    # print("sent syn ack")
    #
    # req_pack = sniff(count=1, filter='tcp port 80')
    # print("get http request")
    #
    # sleep(2)
    # resp_packet(req_pack)
    # print("finished!!!")

    print("hello i am the site server")

    server_site_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_site_tcp.bind(('127.0.0.1', 80))

    server_site_tcp.listen(1)
    print("listening...")

    ans_socket, ans_addr = server_site_tcp.accept()

    request = ans_socket.recv(1024).decode()

    print("got http request")

    http_response = b"HTTP/1.1 200 OK\r\nContent_Type: text/html\r\n\r\n<html><body>.....blablabla....</body></html>"

    ans_socket.sendall(http_response)

    print("sent http response")


    ans_socket.close()
    print("closed socket...")
    print("finished!!!")






