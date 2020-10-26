#!/usr/bin/env python

import logging
import os
import glob
import csv

logger = logging.getLogger("")
consoleHandler = logging.StreamHandler()

#
# Read in OUI into Dictionary
#


def search_dic(oui_file):
    OUILIST = []
    ouilen = 0
    with open('files/' + oui_file) as ouif:
        lines = ouif.readlines()[4:]
    for cnt, line in enumerate(lines):
        if not lines or not '(hex)' in lines[cnt]:  # First block
            continue
        assert '(base 16)' in lines[cnt + 1]

        oui = lines[cnt + 1].split()[0]
        company = lines[cnt + 1].split('\t')[-1]
        street = lines[cnt - 3].strip()
        city = lines[cnt - 2].strip()
        country = lines[cnt - 1].strip()
        OUILIST.append(dict(oui=oui, company=company.rstrip()))
        ouilen = ouilen + 1
    logger.info("Found %s vendors in IEEE OUI file", ouilen)
    return OUILIST

#
# Read in known device list
#


def get_device_list(data_fold):
    vendor = []
    product = []
    mac = []
    DEVLIST = []
    dev_counter = 0
    os.chdir(data_fold)
    for dev_file in glob.glob("*.csv"):
       logger.info("Reading: %s", str(data_fold + dev_file))
       dev_counter = 0
       with open(dev_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Exclude'] != "X":
                    dev_counter += 1
                    logger.debug("%s, %s, %s" %
                             (row['Vendor'], row['Product'], row['MAC']))
                    DEVLIST.append(
                        dict(vendor=row['Vendor'], product=row['Product'], mac=row['MAC']))
            logger.info("Read in %s devices from %s", str(dev_counter), str(dev_file))
    logger.info("Read in %s devices in total", len(DEVLIST))
    return DEVLIST
