#!/usr/bin/env python3
import pandas as pd, numpy as np
import sys

input = sys.argv[1]
output = sys.argv[2]


frame = pd.read_csv(input)

unidentified = 0
total = 0
for index in frame.index:
    entry = frame.loc[index]
    if "NE4110S" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NE4110S"
    elif "NE4110A" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NE4110A"
    elif "NP5410" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5410"
    elif "NP5210" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5210"
    elif "5210" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5210"
    elif "5230" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5230"
    elif "5232" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5232"
    elif "3151" in str(entry["Product"]):
        frame.loc[index,"Product"] = "G3151"
    elif "NP5110A" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5110A"
    elif "3110" in str(entry["Product"]):
        frame.loc[index,"Product"] = "G3110"
    elif "3111" in str(entry["Product"]):
        frame.loc[index,"Product"] = "G3111"
    elif "6150" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP6150"
    elif "5130" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5130"
    elif "5110" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5110"
    elif "4100T" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NE4100T"
    elif "5150" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5150"
    elif "6510" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP6510"
    elif "5610" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5610"    
    elif "3150" in str(entry["Product"]):
        frame.loc[index,"Product"] = "G3150"
    elif "5450" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5450"
    elif "5650" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5650"
    elif "6250" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP6250"
    elif "6450" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP6450"
    elif "6610" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP6610"
    elif "2210" in str(entry["Product"]):
        frame.loc[index,"Product"] = "E2210"
    elif "5104" in str(entry["Product"]):
        frame.loc[index,"Product"] = "5104"
    elif "5004" in str(entry["Product"]):
        frame.loc[index,"Product"] = "5004"
    elif "4110S" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NE4110S"
    elif "5430" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5430"
    elif "3251" in str(entry["Product"]):
        frame.loc[index,"Product"] = "G3251"
    elif "3211" in str(entry["Product"]):
        frame.loc[index,"Product"] = "G3211"
    elif "5250A" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5250A"
    elif "5340" in str(entry["Product"]):
        frame.loc[index,"Product"] = "W5340"
    elif "3170" in str(entry["Product"]):
        frame.loc[index,"Product"] = "MB3170"
    elif "3270" in str(entry["Product"]):
        frame.loc[index,"Product"] = "MB3270"
    elif "3480" in str(entry["Product"]):
        frame.loc[index,"Product"] = "MB3480"
    elif "4120" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NE4120"
    elif "3180" in str(entry["Product"]):
        frame.loc[index,"Product"] = "MB3180"
    elif "5630" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5630"
    elif "6650" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP6650"
    elif "4410A" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP4410A"
    elif "2150" in str(entry["Product"]):
        frame.loc[index,"Product"] = "W2150"
    elif "5312" in str(entry["Product"]):
        frame.loc[index,"Product"] = "W5312"
    elif "4110" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NE4110"
    elif "5250" in str(entry["Product"]):
        frame.loc[index,"Product"] = "NP5250"
    elif "611" in str(entry["Product"]):
        frame.loc[index,"Product"] = "EDS611"
    elif "MiiNePort" in str(entry["Product"]):
        if "E1" in str(entry["Product"]):
            frame.loc[index,"Product"] = "MiiNePort-E1"
        elif "E2" in str(entry["Product"]):
            frame.loc[index,"Product"] = "MiiNePort-E2"
        else:
            unidentified += 1
            print(str(entry["Product"]))
            frame.drop(index, inplace=True)
    else:
        unidentified += 1
        print(str(entry["Product"]))
        frame.drop(index, inplace=True)
    total += 1

print ("Unidentified: " + str(unidentified))
print ("Identified:   " + str(total-unidentified))
print ("Total:        " + str(total))

frame.to_csv(output, sep=',', encoding='utf-8')


