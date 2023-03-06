from random import randint
import socket
from time import sleep

from numpy import character
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP

def server_connection():
    print("Server is running...\n")
    arr = ip_List()
    while True:
        print("pls start the client")

        disco_packet = sniff(count=1, filter='udp and (port 68)')
        print("The server got the discover packet")

        sleep(2)
        offer_packet(disco_packet, arr)
        print("The server has sent the offer packet")

        req_packet = sniff(count=1, filter='udp and (port 68)')
        print("The server got the request packet")

        sleep(2)
        ack_packet(req_packet)
        print("The server has sent the ack packet")

        print("press 1 to continue and 0 to stop")

        if 0 == input():
            break

    return

def offer_packet(disco_packet, arr):
    # ------------Ethernet Layer--------------#
    ether = Ether()
    # ether.src = "08:00:27:d3:c1:00"
    ether.dst = "ff:ff:ff:ff:ff:ff"
    # ether.show()
    # ----------------------------------------#


    # ------------IP Layer--------------#
    ip = IP()
    ip.src = '10.0.2.19'
    ip.dst = '255.255.255.255'
    # ip.show()
    # -----------------------------------#


    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 68
    udp.dport = 67
    # udp.show()
    # -----------------------------------------#


    # ------------Bootp Layer--------------#
    bootp = BOOTP()
    bootp.xid = disco_packet[0][3].xid
    bootp.flags = 2
    bootp.yiaddr = arr[0]
    arr.pop(0)
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
    # ether.src = "08:00:27:d3:c1:00"
    ether.dst = "ff:ff:ff:ff:ff:ff"
    # ether.show()
    # ----------------------------------------#


    # ------------IP Layer--------------#
    ip = IP()
    ip.src = '10.0.2.19'
    ip.dst = '255.255.255.255'
    # ip.show()
    # -----------------------------------#


    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 68
    udp.dport = 67
    # udp.show()
    # -----------------------------------------#


    # ------------Bootp Layer--------------#
    bootp = BOOTP()
    bootp.xid = req_packet[0][3].xid
    bootp.flags = 2
    bootp.sname = "I am the DHCP server"
    # udp.show()
    # --------------------------------------#


    # ------------Application Layer--------------#
    dhcp = DHCP(options=[("message-type", "ack"), "end"])
    # dhcp.show()
    # -------------------------------------------#


    # ------------The Complete Packet--------------#
    dhcp_ack = ether / ip / udp / bootp / dhcp
    # dhcp_offer.show()
    # ---------------------------------------------#

    sendp(dhcp_ack)



def ip_List():
    ip_list = []
    for x in range(20, 201):
        ip_list.append("10.0.2." + str(x))
    return ip_list



if __name__ == "__main__":
    server_connection()







