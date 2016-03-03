import csv
from lineclass4 import *

biglist = []

with open('dadspfirst10.csv','rU') as h:
    reader = csv.reader(h)
    live = False
    for row in reader:
        if live:
            biglist.append(Line(row[0],row[1],row[2],row[3],row[4],row[5],\
                            row[6],row[7],row[8],row[9],0,0))#row[10],row[11]))
        else:
            live = True

stocksinplay = []
for row in biglist:
    stocksinplay.append(row.stock)

def getstocksplitlines(): #Populates stocklines
    r = 'allsplitlines.csv'
    with open(r,'rU') as p:
        reader = csv.reader(p)
        for row in reader:
            if row[1] in stocksinplay:
                biglist.append(SplitLine(row[0],row[1],row[2],row[3]))
getstocksplitlines()

biglist.sort(key = lambda r : r.dateval)
biglist.sort(key = lambda r : r.stock)

with open('dadspfirst10sorted.csv','w') as g:
    writer = csv.writer(g)
    writer.writerow(['Date','Stock','Close','KNO','%'])
    for row in biglist:
        if isinstance(row,Line):
            writer.writerow([row.dateobj.meat,row.stock,row.close,row.kno,row.perc])
        elif isinstance(row,SplitLine):
            writer.writerow([row.dateobj.meat,row.stock,row.splitfrom,row.splitto])
