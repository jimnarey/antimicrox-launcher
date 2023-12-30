#!/usr/bin/env python3

# import sys
import socket
import struct

NETLINK_CONNECTOR = 11
CN_IDX_PROC = 1
CN_VAL_PROC = 1


def parse_msg_header(nlmsg):
    hdr = {}
    hdr["len"], hdr["type"], hdr["flags"], hdr["seq"], hdr["pid"] = struct.unpack(
        "=LHHLL", nlmsg[:16]
    )
    return hdr


def create_nl_socket():
    sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_CONNECTOR)
    sock.bind((0, CN_IDX_PROC))
    return sock


def recv_nl_messages(sock):
    while True:
        try:
            data = sock.recv(65535)
            # data = sock.recv(131070)
            msg_header = parse_msg_header(data)
            print(msg_header)
        except socket.error as e:
            print("Socket error:", e)


def monitor_process_events():
    nl_socket = create_nl_socket()
    if nl_socket:
        try:
            recv_nl_messages(nl_socket)
        finally:
            nl_socket.close()
    else:
        print("Failed to create socket")


if __name__ == "__main__":
    monitor_process_events()
