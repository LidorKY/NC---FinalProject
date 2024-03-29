import random
from random import randint
import socket
from time import sleep

from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


def client_connection():

    print("Client is running...\n")

    discover_packet()
    print("The client has sent the discover packet")

    off_packet = sniff(count=1, filter='udp and (port 67)')
    print("The client got the offer packet")

    sleep(2)
    request_packet(off_packet)
    print("The client has sent the request packet")

    ack_pack = sniff(count=1, filter='udp and (port 67)')
    print("The client got the ack packet")
    return



def discover_packet():
    #------------Ethernet Layer--------------#
    ether = Ether()
    ether.dst = "ff:ff:ff:ff:ff:ff"
    # ---------------------------------------#

    # ------------IP Layer--------------#
    ip = IP()
    ip.src = '0.0.0.0'
    ip.dst = '255.255.255.255'
    # -----------------------------------#

    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 67
    udp.dport = 68
    # -----------------------------------------#

    # ------------Bootp Layer--------------#
    bootp = BOOTP()
    bootp.xid = random.randint(1, pow(2, 32)-1)
    bootp.flags = 1
    # bootp.ciaddr = ip.src
    # bootp.yiaddr =
    bootp.siaddr = "10.0.2.19"
    # bootp.giaddr =
    # ---------------------------------------#
    # ------------Application Layer--------------#
    dhcp = DHCP(options=[("message-type", "discover"), "end"])
    # -------------------------------------------#

    # ------------The Complete Packet--------------#
    dhcp_discover = ether / ip / udp / bootp / dhcp
    # ---------------------------------------------#
    sendp(dhcp_discover)



def request_packet(off_packet):
    # ------------Ethernet Layer--------------#
    ether = Ether()
    ether.dst = "ff:ff:ff:ff:ff:ff"
    # ----------------------------------------#

    # ------------IP Layer--------------#
    ip = IP()
    ip.src = '0.0.0.0'
    ip.dst = '255.255.255.255'
    # ----------------------------------#

    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 67
    udp.dport = 68
    # -----------------------------------------#

    # ------------Bootp Layer--------------#
    bootp = BOOTP()
    bootp.xid = off_packet[0][3].xid
    bootp.flags = 1
    # bootp.ciaddr = ip.src
    # bootp.yiaddr =
    bootp.siaddr = "10.0.2.19"
    # bootp.giaddr =
    # bootp.chaddr = "00:11:22:33:44:55"
    # ---------------------------------------#

    # ------------Application Layer--------------#
    dhcp = DHCP(options=[("message-type", "request"), "end"])
    # -------------------------------------------#

    # ------------The Complete Packet--------------#
    dhcp_request = ether / ip / udp / bootp / dhcp
    # ---------------------------------------------#
    sendp(dhcp_request)




if __name__ == "__main__":
    client_connection()