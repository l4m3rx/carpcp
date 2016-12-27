#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import carpcp_conf as conf

__version__ = '0.999a'
__license__ = 'GPLv3'
__author__ = 'georgi.kolev_[at]_gmail.com'
__name__ = 'carpcplib'


MCAST_PORT = conf.MULTICAST_PORT
MCAST_ADDR = conf.MULTICAST_ADDR


def mcast_send_socket(addr=MCAST_ADDR, port=MCAST_PORT):
    """ Create multicast socket object """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
    return s


def mcast_send(sock, data, addr=MCAST_ADDR, port=MCAST_PORT):
    """ Send data to multicast address """
    return sock.sendto(data, (addr, port))

# EOF