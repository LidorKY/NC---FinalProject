from random import randint
import socket
from scapy.all import *
from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


def client_connection():

    print("Client is running...\n")

    discover_packet()

    off_packet = sniff(count=1, filter='udp and (port 67 or port 68)')

    request_packet(off_packet)

    ack_pack = sniff(count=1, filter='udp and (port 67 or port 68)')


def discover_packet():
    #------------Ethernet Layer--------------#
    ether = Ether()
    ether.src = "00:11:22:33:44:55" #can also use RandMAC() function
    #ether.show()
    # ---------------------------------------#


    # ------------IP Layer--------------#
    ip = IP()
    ip.src = '0.0.0.0'
    # ip.show()
    # -----------------------------------#


    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 67
    udp.dport = 68
    udp.show()
    # -----------------------------------------#


    # ------------Didn't fully understand this Layer--------------#
    bootp = BOOTP()
    bootp.ciaddr = ip.src
    # bootp.yiaddr =
    bootp.siaddr = "10.0.2.15"
    # bootp.giaddr =
    bootp.chaddr = "00:11:22:33:44:55"
    bootp.flags = 1
    # udp.show()
    # ------------------------------------------------------------#


    # ------------Application Layer--------------#
    dhcp = DHCP(options=[("message-type", "discover"), "end"])
    # dhcp.show()
    # -------------------------------------------#


    # ------------The Complete Packet--------------#
    dhcp_discover = ether / ip / udp / bootp / dhcp
    # dhcp_discover.show()
    # ---------------------------------------------#


    sendp(dhcp_discover)



def request_packet(off_packet):
    # ------------Ethernet Layer--------------#
    ether = Ether()
    ether.src = "00:11:22:33:44:55"
    # ether.show()
    # ----------------------------------------#


    # ------------IP Layer--------------#
    ip = IP()
    ip.src = off_packet[0][3].yiaddr
    ip.dst = off_packet[0][1].src
    # ip.show()
    # ----------------------------------#


    # ------------Transport Layer--------------#
    udp = UDP()
    udp.sport = 67
    udp.dport = 68
    # udp.show()
    # -----------------------------------------#


    # ------------Didn't fully understand this Layer--------------#
    bootp = BOOTP()
    bootp.ciaddr = ip.src
    # bootp.yiaddr =
    bootp.siaddr = "10.0.2.15"
    # bootp.giaddr =
    bootp.chaddr = "00:11:22:33:44:55"
    bootp.flags = 1
    # udp.show()
    # ------------------------------------------------------------#


    # ------------Application Layer--------------#
    dhcp = DHCP(options=[("message-type", "request"), "end"])
    # dhcp.show()
    # -------------------------------------------#


    # ------------The Complete Packet--------------#
    dhcp_request = ether / ip / udp / bootp / dhcp
    # dhcp_request.show()
    # ---------------------------------------------#


    sendp(dhcp_request)




if __name__ == "__main__":
    client_connection()