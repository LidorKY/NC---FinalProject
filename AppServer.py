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
from scapy.layers.http import HTTPResponse
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
    ip.dst = req_packet[0][IP].dst

    tcp = TCP()
    tcp.sport = req_packet[0][TCP].dport
    tcp.dport = req_packet[0][TCP].sport
    tcp.flags = "A"
    tcp.seq = 1000
    tcp.ack = 2000

    # http = HTTPResponse()
    # http.Status_Code = 200
    # http.Reason = 'OK'
    # http.HTTP_Version = 'HTTP/1.1'
    # http.date = time.time()
    # http.Server = 'Site_Server'

    html_page = """<html><body>.....blablabla....</body></html>"""

    http = "HTTP/1.1 200 OK\r\nContent_Type: text/html\r\n\r\n" + html_page

    response_packet = ip / tcp / http

    send(response_packet)



if __name__ == "__main__":
    print("hello i am the site server")

    syn_pack = sniff(count=1, filter='tcp port 80')

    sleep(2)
    ack_packet(syn_pack)

    req_pack = sniff(count=1, filter='tcp port 80')

    sleep(2)
    resp_packet(req_pack)
    print("finished!!!")






