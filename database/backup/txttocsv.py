counter = 0

fw = open('lantronix.csv', 'w')
with open('lantronix.txt', 'r') as infile:
    while True:
        lines = []
        for i in range(4):
            lines.append(infile.readline())
        if lines[1]:
            lines[1] = lines[1].rstrip()
            lines[1] = lines[1][12:14]+":"+lines[1][14:16]+":"+lines[1][16:18]+":"+lines[1][18:20]+":"+lines[1][20:22]+":"+lines[1][22:24]
        fw.write(str(lines[0].rstrip()+","+lines[1]+","+lines[2].rstrip()+"\n"))
fw.close()
