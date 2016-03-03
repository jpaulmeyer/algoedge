import csv

x = 'sp500recent.csv'
out = []

with open(x,'rU') as p:
    reader = csv.reader(p)
    for row in reader:
        if row[1] not in out:
            out.append(row[1])

with open('allstocks.csv','w') as q:
    writer = csv.writer(q)
    for i in range(len(out)):
        writer.writerow([out[i]])
