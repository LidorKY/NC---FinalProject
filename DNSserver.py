import nslookup as nslookup
from scapy.all import DNS, DNSQR, IP, sr1, UDP
from random import randint
import socket
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


def server_connection():
    print(conf.iface)





def check():
    # print("0")
    # ether = Ether()
    # ether.src = "08:00:27:d3:c1:ef"


    print("1")
    ip = IP()
    # ip.src = '10.0.2.15'
    ip.dst = '8.8.8.8'

    print("2")
    udp = UDP()
    udp.dport = 53


    print("4")
    dns = DNS()
    dns.rd = 1
    dns.qd = DNSQR(qname='www.google.com')

    print("5")
    dns_request = ip / udp / dns

    print("6")
    sent = sr1(dns_request, verbose=0)
    print(sent.summary())

    # print("7")
    # response_packet = sniff(count=1, filter='udp and (port 53)')

    # print("8")
    # response_packet.show()



def response():
    hello = 6



if __name__ == "__main__":
    # server_connection()
    # check()
    check = socket.getaddrinfo("geeksforgeeks.org", 53)
    print(check)
    # check[0][]