import random
from scapy.all import DNS, DNSQR, IP, sr1, UDP
from random import randint
import socket
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


def client_connection():
    print("Hello I am the client")
    query_packet()

    response_packet = sniff(count=1, filter='udp port 53')
    print("client end")
    return




def query_packet():
    #-----------------IP Layer---------------#
    ip = IP()
    ip.src = RandIP()
    ip.dst = '10.0.2.5'
    #----------------------------------------#

    #-----------------Transport Layer---------------#
    udp = UDP()
    udp.dport = 53
    #----------------------------------------------

    #-----------------Application Layer---------------#
    dns = DNS()
    dns.id = random.randint(1, pow(2, 16)-1)
    dns.qr = 0
    dns.opcode = 0
    dns.rd = 1
    dns.qd = DNSQR()
    dns.qd.qname = input("Please enter the site name - example.com: \n")
    # ------------------------------------------------#

    #-----------------The Complete Packet---------------#
    dns_request = ip / udp / dns
    #---------------------------------------------------#
    send(dns_request)


if __name__ == "__main__":
    client_connection()

