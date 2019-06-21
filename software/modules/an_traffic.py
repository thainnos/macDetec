#!/usr/bin/env python

import os
import logging
import pcapy
import dpkt
import binascii
import socket
from struct import unpack
from dpkt.compat import compat_ord

logger = logging.getLogger("")
consoleHandler = logging.StreamHandler()

#
# Listen on Interface
#


def network_capture(pcap_file, dumper, interface):
    mac_addresses = []
    counter = 0
    ipcounter = 0
    tcpcounter = 0
    udpcounter = 0
    devcounter = 0
    # list all devices
    devices = pcapy.findalldevs()
    logging.info('Read the following devices: %s', devices)

    # list avialable network interfaced
    logging.info('Following devices are available: %s', devices)

    logging.info('Sniffing on following device: %s', interface)

    cap = pcapy.open_live(interface, 65536, 1, 0)

    logging.info('Starting sniffing.. Stopping with ctrl+c')
    # time.sleep(5)

    # start sniffing packets for the count of capturing
    #f = open('capture.pcap', 'w')
    dumper = cap.dump_open("capture.pcap")

    while True:
        try:
            (header, packet) = cap.next()
            dumper.dump(header, packet)
        except KeyboardInterrupt:
            break  # stop listening on the interface


#
# Read Pcap File
#
def read_pcap(pcap_file):
    mac_addresses = []
    counter = 0
    ipcounter = 0
    tcpcounter = 0
    udpcounter = 0
    devcounter = 0
    PCAPLIST = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path+"/../")
    pcap_size = os.path.getsize(pcap_file) >> 20
    logging.info('Reading from PCAP file: %s with size %sMB',
                 pcap_file, pcap_size)
    if pcap_size > 10:
        logging.warning(
            'PCAP file is greater than 10MB (%sMB), taking some time', pcap_size)
    for ts, pkt in dpkt.pcap.Reader(open(pcap_file, 'rb')):
        counter += 1
        s_addr = []
        d_addr = []
        eth = dpkt.ethernet.Ethernet(pkt)
        src_mac = str(mac_addr(eth.src))
        dst_mac = str(mac_addr(eth.dst))
        if eth.type == dpkt.ethernet.ETH_TYPE_IP:

            ip = eth.data
            ipcounter += 1
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                tcpcounter += 1
            if ip.p == dpkt.ip.IP_PROTO_UDP:
                udpcounter += 1

            eth_length = 14

            eth_header = pkt[:eth_length]
            eth = unpack('!6s6sH', eth_header)
            eth_protocol = socket.ntohs(eth[2])

            # Parse IP packets, IP Protocol number = 8
            if eth_protocol == 8:
                # Parse IP header
                # take first 20 characters for the ip header
                ip_header = pkt[eth_length:20 + eth_length]

                # now unpack them :)
                iph = unpack('!BBHHHBBH4s4s', ip_header)

                version_ihl = iph[0]
                version = version_ihl >> 4
                ihl = version_ihl & 0xF

                iph_length = ihl * 4

                ttl = iph[5]
                protocol = iph[6]
                s_addr = socket.inet_ntoa(iph[8])
                d_addr = socket.inet_ntoa(iph[9])

        if str(src_mac) not in mac_addresses:
            mac_addresses.append(str(src_mac))
            if s_addr:
                logging.debug('MAC found: %s IP: %s', str(src_mac), str(s_addr))
                PCAPLIST.append(dict(mac=str(src_mac), ip=str(s_addr)))
            else:
                PCAPLIST.append(dict(mac=str(src_mac), ip=0))
                logging.debug('Only MAC found: %s', str(src_mac))
            devcounter = devcounter + 1
        if str(dst_mac) not in mac_addresses:
            mac_addresses.append(str(dst_mac))
            if d_addr:
                logging.debug('MAC found: %s IP: %s', str(dst_mac), str(d_addr))
                PCAPLIST.append(dict(mac=str(dst_mac), ip=str(d_addr)))
            else:
                PCAPLIST.append(dict(mac=str(dst_mac), ip=0))
                logging.debug('Only MAC found: %s', str(dst_mac))
            devcounter = devcounter + 1
    logging.info('Total number of devices found in pcap file: %s', devcounter)
    logging.info('Total number of packets in the pcap file: %s', counter)
    logging.info('Total number of ip packets: %s', ipcounter)
    logging.info('Total number of tcp packets: %s', tcpcounter)
    logging.info('Total number of udp packets: %s', udpcounter)
    return PCAPLIST

#
# Convert a MAC address to a readable/printable string
#


#def mac_addr(address):
#    mac_lst = []
#    for i in range(0, len(binascii.hexlify(address)), 2):
#        mac_lst.append(binascii.hexlify(address)[i:i + 2])
#    mac = ':'.join(str(mac_lst))
#    print(mac)
#i    return mac

def mac_addr(address):
    """Convert a MAC address to a readable/printable string
       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)
