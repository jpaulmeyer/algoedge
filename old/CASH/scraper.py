import urllib2
import csv
from string import find,split
from lineclass4 import *
from dateclass import *

a9 = urllib2.urlopen("http://google.com/").read()

testurl = 'https://www.stocksplithistory.com/?symbol='


def search(symbol,needle):
    html = urllib2.urlopen(testurl + symbol).read()
    for i in range(len(html)-len(needle)):
        if html[i:i+len(needle)] == needle:
            return i+len(needle)

def search2(lst,needle):
    for i in range(len(lst)-len(needle)):
        if lst[i:i+len(needle)] == needle:
            return i+len(needle)


def processdate(datestring):
    
    year = datestring[-4:]
    day = datestring[-8:-6]
    play = datestring[0:-9]
    def reversify(word):
        new = list(word)
        new.reverse()
        out = ''
        for char in new:
            out += char
        return out
    new2 = reversify(play)
    def stripend(word):
        out = ''
        for char in word:
            if char == ' ':
                return out
            else:
                out += char
        return out
    clean = stripend(new2)
    month = reversify(clean)
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    def monthnum(month):
        if month in months:
            return months.index(month) + 1
        #if month not in months:
            #print "Error: Not a month"
            #print month
        return -1
    num = monthnum(month)
    return (num,int(day),int(year))

def datestringify(datetuple):
    yearr = -1
    year = str(datetuple[2]%100)
    if str(datetuple[2]%100) < 10:
        yearr = '0' + year
    else:
        a = str(datetuple[2])
        b = a[-2:]
        yearr = b
    if int(yearr) > 40:
        yearr = '19' + yearr
    else:
        yearr = '20' + yearr
    datee = str(datetuple[0]) + '/' + str(datetuple[1]) + '/' + str(yearr)
    return datee

def processsplits(splittext,dateline,symbol):
    lst = splittext.split(' ')
    return SplitLine(dateline,symbol,lst[2],lst[0])

#b9 = '<table border="0" width="208" style="font-family: Arial; font-size: 12px" cellspacing="0" cellpadding="0">'

def scrapesplit(symbol,outputfile):
    html = urllib2.urlopen(testurl + symbol).read()
    targ1 = '<td width="420" valign="top" align="left"><font face="Arial" size="2"><img width="400" height="40" src='
    targ2 = 'W'
    text = html[search(symbol,targ1):search2(symbol,targ2)]
    clean = text[0:search2(text,'<img')]   
    numsplits = 0
    a = search2(clean,'splits in our <strong>') - 24
    numsplits = clean[a]
    cleaner = clean[search2(clean,'database. '):]
    splitted = cleaner.split("{}'s".format(symbol.upper()))
    out = []
    lsts = []
    for i in range(len(splitted)):
        current = splitted[i]
        a = current.split('.')
        lsts.append(a)
    lsts2 = []
    for i in range(len(lsts)):
        lsts2.append(lsts[i][0:2])
    dates = []
    splits = []
    for i in range(len(lsts2)):
        dates.append(lsts2[i][0][25:])
        splits.append(lsts2[i][1][13:][:search2(lsts2[i][1][13:],' split')][0:-6])
    clean_dates = []
    clean_splits = []
    for split in splits:
        out = ''
        for char in split:
            if char != '\r':
                if char != '\n':
                    out += char
        clean_splits.append(out)
    for date in dates:
        clean_dates.append(processdate(date))
    datelines = []
    for date in clean_dates:
        datelines.append(datestringify(date))
    splitlines = []
    for i in range(len(clean_splits)):
        splitlines.append(processsplits(clean_splits[i],datestringify(clean_dates[i]),symbol))

    return splitlines


    
def scrapeallsplits(stocklist,outputfile):
    uppers = []
    for stock in stocklist:
        uppers.append(stock.upper())
    alll = []
    for stock in uppers:
        try:
            print stock
            alll += scrapesplit(stock,outputfile)
        except:
            continue
    #alll.sort(key = lambda r:r.stock)
    with open(outputfile, 'w') as h:
        writer = csv.writer(h)
        for splitline in alll:
            writer.writerow([splitline.dateline,splitline.stock,splitline.splitfrom,splitline.splitto])
    


stocklist9 = ['aa','cat','ibm','a','abc','abt','yum','aapl','ko','anf','gap','pzza','cake','sbux','cbrl']

stockz9 = []
c9 = 'IBDcurrvals.csv'
def populatestocks(name):
    with open(name,'rU') as p:
        reader = csv.reader(p)
        for row in reader:
            stockz9.append(row[0])
stockz9.sort()

#ACTION LINEs
populatestocks('allstocks.csv')
scrapeallsplits(stockz9,'bunchasplits.csv')











