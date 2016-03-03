import csv
import ystockquote

#IMPORT CSV INTO LINES
lines = []
with open('dadsstocks.csv','rU') as a:
    reader = csv.reader(a)
    live = False
    for row in reader:
        if live:
            lines.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],\
                         row[7],row[8],row[9],row[10],row[11],row[12],row[13],\
                         row[14],row[15],row[16]])
        else:
            live = True

#HOW MANY STOCKS DO I HAVE TO BUY
acc = 0
seen = []
repeats = 0

for line in lines:
    if not (line[3] in seen):
        seen.append(line[3])
        acc += 1
    else:
        repeats += 1

print "Repeats: " + str(repeats)
print "Total number of stocks to buy: " + str(acc)
print "\n"

#MAKE A DICT OF (STOCK : [LINE,LINE,LINE,ETC])
stockdict = {}

for line in lines:
    b = stockdict.keys()
    if line[3] in b:
        stockdict[line[3]].append(line)
    else:
        stockdict[line[3]] = [line]

#SETUP OUTPUT
c = stockdict.keys()
c.sort()
outs = []
for stock in c:
    #ADD KNOS
    out = [stock]
    for line in stockdict[stock]:
        out.append(line[5])
    outs.append(out)
    #ADD PRICE AT FIRST KNO WHILE AGO
    outs.append([stock,line[4]])
    #ADD PRICE NOW
    print "Current Stock: " + stock
    #outs.append([stock,ystockquote.get_price(stock)])

#WRITE OUTPUT
with open('sp500knos.csv','w') as d:
    writer = csv.writer(d)
    for line in outs:
        writer.writerow(line)






