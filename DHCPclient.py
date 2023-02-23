from random import randint

from scapy.all import *

from scapy.layers import dhcp
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


def dicover_packet():
    ether = Ether()
    ether.dst = "08:00:27:d3:c1:ef"
    ether.show()

    ip = IP()
    ip.dst = "127.0.0.1"
    ip.show()

    udp = UDP()
    udp.sport = 67
    udp.dport = 68
    udp.show()

    bootp = BOOTP()
    bootp.flags = 1
    udp.show()

    dhcp = DHCP(options=[("message-type", "discover"), "end"])
    dhcp.show()

    dhcp_discover = ether / ip / udp / bootp / dhcp
    dhcp_discover.show()

    sendp(dhcp_discover)


if __name__ == "__main__":
    dicover_packet()