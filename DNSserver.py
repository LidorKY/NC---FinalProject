
import nslookup as nslookup
from scapy.all import DNS, DNSQR, IP, sr1, UDP, sendp, send, sniff, sndrcv
from random import randint
import socket
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


def server_connection():
    print("Hello I am the DNS server")
    que_packet = sniff(count=1, filter='udp port 53')
    print("sniffed packet")


    response_packet(que_packet)
    print("server sent response")


def response_packet(que_packet):
    ip = IP()
    ip.src = '192.168.0.5'
    ip.dst = que_packet[0][1].src

    udp = UDP()
    udp.sport = que_packet[0][2].dport
    udp.dport = que_packet[0][2].sport

    dns = DNS()
    dns.id = que_packet[0][3].id
    dns.qr = 1
    dns.rd = 1
    dns.ra = 1

    dns.qd = que_packet[0][3].qd
    dns.an = DNSRR()
    dns.an.rrname = que_packet[0][3].qd.qname
    dns.an.rdata = socket.getaddrinfo(dns.an.rrname, 53)
    dns.an.type = 'A'

    dns_response = ip / udp / dns
    print("here")
    send(dns_response)




if __name__ == "__main__":
    server_connection()
