#!/usr/bin/env python
import os
import time
from urllib.request import urlopen
import logging
import json
import sys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger("")
consoleHandler = logging.StreamHandler()

#
# Check if OUI exists and is not older than one day
#


def get_mac_table_ieee(filename="files/oui.txt", oui_url=[], oui_time=0):
    if os.path.isfile('files/oui.txt'):
        difftime = time.time() - os.path.getmtime('files/oui.txt')
    else:
        oui_time = 0
        difftime = 1
    # if oui file is to old or oui_time == 0 then download it
    if (int(difftime) > int(oui_time * 60 * 60 * 24)) or (oui_time == "0"):
        logger.info("Downloading IEEE MAC Vendor list")
        file_name = oui_url.split('/')[-1]
        u = urlopen(oui_url)
        f = open('files/' + file_name, 'wb')
        meta = u.info()
        file_size = int(u.getheader("Content-Length"))
        logger.info("Downloading: %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 65536
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d [%3d%%]" % (
                file_size_dl, file_size_dl * 100. / file_size)
            logger.info(('Download %s ' % status))
            sys.stdout.flush()
        f.close()
        logging.info("Download finished")
    else:
        logging.info("IEEE MAC Vendor list is up to date")

#
# Check if vunlerability database exists and download it
#


def get_vulns(filename, vuln_time=0, CVELIST=[]):
    vuln_count = 0
    filename = filename.strip()  # remove spaceing
    if os.path.isfile('files/' + filename + '.json'):
        difftime = time.time() - os.path.getmtime('files/' + filename + '.json')
    else:
        vuln_time = 0
        difftime = 1
    # if vuln file is to old or vuln_time == 0 then download it
    if (int(difftime) > int(vuln_time * 60 * 60 * 24)) or (vuln_time == "0"):
        logger.info("Downloading vulnerable database for %s", filename)
        url = 'https://localhost/api/search/' + filename
        logging.info("Fetching %s", url)
        content = urlopen(url).read()
        f = open('files/' + filename + '.json', 'wb')
        f.write(content)
        f.close()
    else:
        logging.info("Vuln list for vendor %s is up to date", filename)

    vuln_json = json.load(open('files/' + filename + ".json"))
    for vuln in vuln_json['data']:
        vuln_count = vuln_count + 1
        logger.debug("---------------------------------------------")
        logger.debug("ID: %s", vuln['id'])
        logger.debug("Summary: %s", vuln['summary'])
        for cpe in vuln['vulnerable_configuration']:
            logger.debug("CPE: %s", cpe)
            CVELIST.append(
                dict(cpe=cpe, vid=vuln['id'], summary=vuln['summary']))
    logger.info("Read in %s vulnerabilities for vendor %s",
                vuln_count, filename)
