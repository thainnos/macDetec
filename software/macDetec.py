#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Passive Device Identification              #
# MAC -> Device                              #
#                                            #
##############################################
import os
import csv
from urllib.request import urlopen
import time
import sys
import re
import dpkt
import json
import logging
import logging.handlers
import pkg_resources
import binascii
import socket
import glob
import pcapy
import ctypes
from struct import unpack
sys.path.append('./modules')
from modules import dl_database
from modules import an_database
from modules import an_traffic
from modules import an_mac

logger = logging.getLogger("")
consoleHandler = logging.StreamHandler()
import coloredlogs
coloredlogs.install(level=logging.INFO)

parse_file = []
capturing = []
pcap_file = []
interface = []
data_fold =[]
oui_file = []
oui_url = []
oui_time = []
vuln_time = []
vuln_vendors = []
CVELIST = []
PCAPLIST = []
dumper = []

# Path for log file
logPath = "./"
# log file name
logFile = "debug"

#
# Function to set the logger and logging level
#
def set_logger():
    # remove old logfile
    try:
        os.remove("{0}/{1}.log".format(logPath, logFile))
    except:
        pass

    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)-80s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, logFile))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)


#
# Creates a config file with default values
#
def createDefaultConfig(path):
    with open(path, "w") as file:
        config = {
            "parse_file": "true",
            "log_level": "info",
            "capturing": "2",
            "pcap_file": "../40_Pcap/4SICS-GeekLounge-151021.pcap",
            "data_fold": "../30_Database/",
            "interface": "wlp3s0",
            "oui_file": "oui.txt",
            "oui_url": "http://standards-oui.ieee.org/oui.txt",
            "oui_time": "1",
            "vuln_time": "1",
            "vuln_vendors": "siemens, moxa, phoenix, lantronix, micronics, crouzet, wago, hirschmann"}
        json.dump(config, file, indent=2)

#
# Read Config File and set global paramaters
#


def read_config():
    global parse_file
    global capturing
    global pcap_file
    global interface
    global data_fold
    global oui_file
    global oui_url
    global oui_time
    global vuln_time
    global vuln_vendors

    config_file_path = "config.json"
    if not os.path.isfile(config_file_path):
        createDefaultConfig(config_file_path)

    # Parse configuration file
    with open(config_file_path) as config_file:
        config_data = json.load(config_file)
    parse_file = config_data["parse_file"]
    capturing = config_data["capturing"]
    pcap_file = config_data["pcap_file"]
    interface = config_data["interface"]
    oui_file = config_data["oui_file"]
    oui_url = config_data["oui_url"]
    oui_time = config_data["oui_time"]
    vuln_time = config_data["vuln_time"]
    vuln_vendors = config_data["vuln_vendors"]
    log_level = config_data["log_level"]
    data_fold = config_data["data_fold"]

    if log_level == "info":
        consoleHandler.setLevel(logging.INFO)
    elif log_level == "warning":
        consoleHandler.setLevel(logging.WARNING)
    else:
        consoleHandler.setLevel(logging.DEBUG)
    pass

#
# Check dependencies
# TODO: not complete


def check_dependencies():
    # check for root and dependencies

    if parse_file == "false":
        if not os.geteuid() == 0:
            logging.critical('MAC Detec must be run as root, required by:')
            logging.critical('  - sniffing')
            sys.exit()
    if not pkg_resources.get_distribution("dpkt").version >= "1.0.0":
        logging.critical('dpkt Version >= 1.0.0. required')
        sys.exit()
    #if not pkg_resources.get_distribution("scapy").version >= "2.3.3":
    #    logging.critical('Scapy Version >= 2.3.3 required')
        #sys.exit()
    if not pkg_resources.get_distribution("pcapy").version >= "0.11.1":
        logging.critical('Pcapy Version >= 0.11.1 required')
        sys.exit()
    pass


#
# Main function
#
if __name__ == "__main__":
    set_logger()
    logging.info('.-------------------------------------.')
    logging.info('| MAC Detec started                   |')
    logging.info('+-------------------------------------+')
    logging.info('| HH  HH   SSSSS   AAAA  Hochschule   |')
    logging.info('| HH  HH  SS      AA  AA Augsburg     |')
    logging.info('| HHHHHH   SSSS   AAAAAA              |')
    logging.info('| HH  HH      SS  AA  AA              |')
    logging.info('| HH  HH  SSSSS   AA  AA              |')
    logging.info('+-------------------------------------+')
    logging.info('| Matthias.Niedermaier@hs-augsburg.de |')
    logging.info('| Thomas.Hanka@hs-augsburg.de         |')
    logging.info('| Sven.Plaga@aisec.fraunhofer.de      |')
    logging.info('| Dominik.Merli@hs-augsburg.de        |')
    logging.info('| Alexander.vonBodisco@hs-augsburg.de |')
    logging.info('*-------------------------------------*')
    logger.info("Reading config file")
    read_config()
    logger.info("Checking dependencies")
    check_dependencies()
    logger.info("Checking IEEE MAC VENDOR List")
    dl_database.get_mac_table_ieee(oui_url=oui_url, oui_time=oui_time)
    logger.info("Download vulnerability databases")
    for vuln_vendor in vuln_vendors.split(','):
        dl_database.get_vulns(vuln_vendor, vuln_time, CVELIST)
    logger.info("Reading OUI MAC VENDOR List")
    OUILIST = an_database.search_dic(oui_file)
    logger.info("Parsing DEVICE list")
    DEVLIST = an_database.get_device_list(data_fold)
    if parse_file == "false":
        logger.info("Live capture on %s", interface)
        an_traffic.network_capture(pcap_file, dumper, interface)
        logger.info("Reading PCAP File")
        PCAPLIST = an_traffic.read_pcap("capture.pcap")
        logger.info("Compare pcap with OUI and device list")
        an_mac.comp_all(CVELIST, PCAPLIST, OUILIST, DEVLIST)
    else:
        logger.info("Reading PCAP File")
        PCAPLIST = an_traffic.read_pcap(pcap_file)
        logger.info("Compare pcap with OUI and device list")
        an_mac.comp_all(CVELIST, PCAPLIST, OUILIST, DEVLIST)
