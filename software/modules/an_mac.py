#!/usr/bin/env python

import logging
import re

logger = logging.getLogger("")
consoleHandler = logging.StreamHandler()


#
# Compare Lists and Entrys - MAC Distance
#
def comp_all(CVELIST, PCAPLIST, OUILIST, DEVLIST):
    # TODO: use function
    FCVELIST = []
    for pcapentry in PCAPLIST:
        for pcapkey, pcapvalue in pcapentry.items():
            FCVELIST = []
            if pcapkey == "mac":
                mac_distance = 0
                # Mac Distance FFFFFF is the a vendor group
                min_mac_distance = int("FFFFFF", 16)
                min_mac_product = ""
                min_mac_vendor = ""
                p_mac = pcapvalue[0:2] + pcapvalue[3:5] + pcapvalue[6:8]
                for ouientry in OUILIST:
                    for ouikey, ouivalue in ouientry.items():
                        if ouikey == "oui":
                            if ouivalue == p_mac.upper():
                                logger.info(
                                    "################################################################################################")
                                logger.info("Device IP:      %s",
                                            pcapentry.get('ip'))
                                logger.info("Device MAC:     %s",
                                            pcapentry.get('mac').upper())
                                logger.info("OUI Match:      %s", ouivalue)
                                logger.info("Vendor:         %s",
                                            ouientry.get('company'))

                                for refdev in DEVLIST:
                                    for devkey, devvalue in refdev.items():
                                        if devkey == "mac":
                                            devvalue = devvalue.replace(
                                                ":", "")
                                            pcapvalue = pcapvalue.replace(
                                                ":", "")
                                            mac_distance = int(
                                                devvalue, 16) - int(pcapvalue, 16)
                                            if min_mac_distance > abs(mac_distance):
                                                min_mac_distance = abs(
                                                    mac_distance)
                                                min_mac_product = refdev.get(
                                                    'product')
                                                min_mac_vendor = refdev.get(
                                                    'vendor')
                                logger.info("------------------")
                                logger.info("?Product?:      %s",
                                            min_mac_product)
                                logger.info("?Vendor?:       %s",
                                            min_mac_vendor)
                                logger.info("?Distance?:     0x%s", hex(
                                    min_mac_distance)[2:].zfill(6).upper())
                                product_nrs = re.findall(
                                    r'\d+', min_mac_product)
                                product_ven = min_mac_vendor.split()
                                product_ven = [item.lower()
                                               for item in product_ven]
                                for product_nr in product_nrs:
                                    # TODO: Comparision CPE ...
                                    if len(product_nr) >= 3:
                                        for refcve in CVELIST:
                                            for devkey, devvalue in refcve.items():
                                                if devkey == "cpe":
                                                    if product_nr in devvalue:
                                                        if refcve.get('vid') not in FCVELIST:
                                                            if any(s in devvalue for s in product_ven):
                                                                logger.info(
                                                                    "------------------")
                                                                logger.info(
                                                                    "?Possible CPE?: %s", devvalue)
                                                                logger.info(
                                                                    "?Possible CVE?: %s", refcve.get('vid'))
                                                                logger.info(
                                                                    "?Possible SUM?: %s", refcve.get('summary')[:80])
                                                                logger.info("?Possible SUM?: %s", refcve.get(
                                                                    'summary')[80:160])
                                                                FCVELIST.append(
                                                                    refcve.get('vid'))
    logger.info(
        "################################################################################################")
