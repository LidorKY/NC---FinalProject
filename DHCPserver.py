from random import randint
import socket
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP

def server_connection():

    print("Server is running...\n")

    disco_packet = sniff(count=1, filter='udp and (port 67 or port 68)')

    offer_packet(disco_packet)

    req_packet = sniff(count=1, filter='udp and (port 67 or port 68)')

    ack_packet(req_packet)


def offer_packet(disco_packet):
    # ------------Ethernet Layer--------------#
    ether = Ether()
    ether.src = "08:00:27:d3:c1:ef"
    ether.dst = disco_packet[0][0].src
    # ether.show()
    # ----------------------------------------#


    # ------------IP Layer--------------#
    ip = IP()
    ip.src = '10.0.2.15'
    ip.dst = disco_packet[0][1].src
    # ip.show()
    # -----------------------------------#


    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 68
    udp.dport = 67
    # udp.show()
    # -----------------------------------------#


    # ------------Didn't fully understand this Layer--------------#
    bootp = BOOTP()
    bootp.flags = 2
    bootp.yiaddr = "192.168.1.1"
    bootp.sname = "I am the DHCP server"
    # udp.show()
    # ------------------------------------------------------------#


    # ------------Application Layer--------------#
    dhcp = DHCP(options=[("message-type", "offer"), "end"])
    # dhcp.show()
    # -------------------------------------------#


    # ------------The Complete Packet--------------#
    dhcp_offer = ether / ip / udp / bootp / dhcp
    # dhcp_offer.show()
    # ---------------------------------------------#


    sendp(dhcp_offer)

def ack_packet(req_packet):
    # ------------Ethernet Layer--------------#
    ether = Ether()
    ether.src = "08:00:27:d3:c1:ef"
    ether.dst = req_packet[0][0].src
    # ether.show()
    # ----------------------------------------#


    # ------------IP Layer--------------#
    ip = IP()
    ip.src = '10.0.2.15'
    ip.dst = req_packet[0][1].src
    # ip.show()
    # -----------------------------------#


    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 68
    udp.dport = 67
    # udp.show()
    # -----------------------------------------#


    # ------------Didn't fully understand this Layer--------------#
    bootp = BOOTP()
    bootp.flags = 2
    bootp.sname = "I am the DHCP server"
    # udp.show()
    # ------------------------------------------------------------#


    # ------------Application Layer--------------#
    dhcp = DHCP(options=[("message-type", "ack"), "end"])
    # dhcp.show()
    # -------------------------------------------#


    # ------------The Complete Packet--------------#
    dhcp_ack = ether / ip / udp / bootp / dhcp
    # dhcp_offer.show()
    # ---------------------------------------------#

    sendp(dhcp_ack)





if __name__ == "__main__":
    server_connection()







