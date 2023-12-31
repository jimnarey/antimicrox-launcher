#!/usr/bin/env python3

import sys
import socket
import struct


NETLINK_CONNECTOR = 11
CN_IDX_PROC = 1
CN_VAL_PROC = 1


PROC_EVENT_TYPES = {
    1: 'fork',
    2: 'exec',
    2147483648: 'exit'
}


def parse_msg_header(nlmsg):
    hdr = {}
    hdr["len"], hdr["type"], hdr["flags"], hdr["seq"], hdr["pid"] = struct.unpack(
        "=LHHLL", nlmsg[:16]
    )
    return hdr


def get_event_data(nlmsg):
    event_data = {
        'pid': int.from_bytes(nlmsg[56:60], byteorder=sys.byteorder),
        'event': int.from_bytes(nlmsg[36:40], byteorder=sys.byteorder)}
    return event_data


def analyse_msg(nlmsg):
    for i in range(16, len(nlmsg) - 3, 4):
        print('-----------')
        print(i)
        num = int.from_bytes(nlmsg[i:i + 4], byteorder=sys.byteorder)
        print(num)
        if num == 1:
            print('FORK')
        if num == 2:
            print('EXEC')


def create_nl_socket():
    sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_CONNECTOR)
    sock.bind((0, CN_IDX_PROC))
    return sock


def recv_nl_messages(sock):
    while True:
        try:
            nlmsg = sock.recv(4096)
            event_data = get_event_data(nlmsg)
            print(event_data)
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
