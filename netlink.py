#!/usr/bin/env python3

import socket
import struct

NETLINK_PROTOCOL = 11
PROCESS_INDEX = 1
# PROCESS_VALUE = 1

NLMSG_ERROR = 0x2

NLMSG_HDRLEN = struct.calcsize("=LHHLL")


def create_nl_socket():
    sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_PROTOCOL)
    sock.bind((0, PROCESS_INDEX))
    return sock


def recv_nl_message(sock):
    while True:
        data = sock.recv(65535)
        nlmsghdr = data[:NLMSG_HDRLEN]
        msg_type, _, _, _, _ = struct.unpack("=LHHLL", nlmsghdr)
        if msg_type == NLMSG_ERROR:
            break
        yield data


def monitor_process_events():
    nl_socket = create_nl_socket()
    try:
        for msg in recv_nl_message(nl_socket):
            print("Received:", msg)
    finally:
        nl_socket.close()


if __name__ == "__main__":
    monitor_process_events()