import csv

stoof = []

with open('truesp500.csv', 'rU') as a:
    reader = csv.reader(a)
    live=False
    for row in reader:
        if live:
            stoof.append(row)
        else:
            live=True
sp500 = []

for row in stoof:
    sp500.append(['1/1/1993',row[1]])

with open('my_sp500.csv', 'w') as b:
    writer = csv.writer(b)
    writer.writerow(['date','sid'])
    for row in sp500:
        writer.writerow(row)
