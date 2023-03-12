from time import sleep
from scapy.all import DNS, DNSQR, IP, sr1, UDP, sendp, send, sniff, sndrcv
from random import randint
import socket
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


my_dictionary = dict()


def server_connection():
    print("Hello I am the DNS server")
    while True:
        print("---sniffing---\n")
        que_packet = sniff(count=1, filter='udp port 53')
        print("sniffed packet\n")

        if srever_cache(que_packet) == True:
            print("from cache\n")
        else:
            sleep(1)
            response_packet(que_packet)
            print("server sent response\n")

        if "stop" == input("if you want to stop pls write stop: \n"):
            return

    print("server end")
    return


def srever_cache(que_packet):
    if que_packet[0][3].qd.qname in my_dictionary:
        # -----------------IP Layer---------------#
        ip = IP()
        ip.src = '10.0.2.5'
        ip.dst = que_packet[0][1].src
        # ----------------------------------------#

        # -----------------Transport Layer---------------#
        udp = UDP()
        udp.sport = que_packet[0][2].dport
        udp.dport = que_packet[0][2].sport
        # -----------------------------------------------#

        # -----------------Application Layer---------------#
        dns = DNS()
        dns.id = que_packet[0][3].id
        dns.qr = 1
        dns.rd = 1
        dns.ra = 1
        dns.qd = que_packet[0][3].qd
        dns.an = DNSRR()
        dns.an.rrname = que_packet[0][3].qd.qname
        dns.an.rdata = my_dictionary[que_packet[0][3].qd.qname]
        # ------------------------------------------------#

        # -----------------The Complete Packet---------------#
        dns_response = ip / udp / dns
        # ---------------------------------------------------#
        send(dns_response)
        return True

    else:
        return False



def response_packet(que_packet):
    # -----------------IP Layer---------------#
    ip = IP()
    ip.src = '10.0.2.5'
    ip.dst = que_packet[0][1].src
    # ----------------------------------------#

    # -----------------Transport Layer---------------#
    udp = UDP()
    udp.sport = que_packet[0][2].dport
    udp.dport = que_packet[0][2].sport
    # -----------------------------------------------#

    # -----------------Application Layer---------------#
    dns = DNS()
    dns.id = que_packet[0][3].id
    dns.qr = 1
    dns.rd = 1
    dns.ra = 1
    dns.qd = que_packet[0][3].qd
    dns.an = DNSRR()
    dns.an.rrname = que_packet[0][3].qd.qname
    dns.an.rdata = socket.getaddrinfo(dns.an.rrname, 53)[0][4][0].split()[0]
    my_dictionary[que_packet[0][3].qd.qname] = dns.an.rdata
    # ------------------------------------------------#

    # -----------------The Complete Packet---------------#
    dns_response = ip / udp / dns
    # ---------------------------------------------------#
    send(dns_response)



if __name__ == "__main__":
    server_connection()