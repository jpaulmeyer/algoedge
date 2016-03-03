#report.py

import csv
position = 10000

class Date(object):

    def __init__(self, datestring):
        self.meat = datestring
        self.month = None
        self.day = None
        self.year = None
        current = ''
        counter = 1
        #processes datestring
        for i in range(len(self.meat)):
            if counter == 3:
                self.year = self.meat[i:len(self.meat)]
                break
            if self.meat[i] != '/':
                current += self.meat[i]
                continue
            elif self.meat[i] == '/':
                if counter == 1:
                    self.month = current
                elif counter == 2:
                    self.day = current
                current = ''
                counter += 1
        self.month = int(self.month)
        self.day = int(self.day)
        self.year = int(self.year)

        #assume everything is after 1940
        if self.year < 40:
            self.year += 2000
        elif self.year >= 40:
            self.year += 1900
        self.dateval = 0 #days since day one sorta
        self.dateval += (self.year - 1940)*365.25
        self.dateval += self.month*31
        self.dateval += self.day

    def days_1jan1940(self):
        out = 0
        m = self.month
        d = self.day
        y = int(self.year)
        y1940 = y - 1940
        mod = y1940 % 4
        if mod == 0 and m > 2:
            out += 1
        out += int((y1940 - mod)*365.25)
        out += 365*mod
        months = [31,28,31,30,31,30,31,31,30,31,30]
        out += sum(months[:(m-1)])
        return out + d - 1

        #self.dateval is what you sort on

class LogLine(object):
    
    def __init__(self,addsub,dateline,stock,price,amt,numshares,cashspentmade,cashafter):
        self.addsub = addsub
        self.dateobj = Date(dateline)
        self.stock = stock
        self.price = float(price)
        self.amt = float(amt)
        self.numshares = float(numshares)
        self.cashspentmade = float(cashspentmade)
        self.cashafter = cashafter

# POPULATE CASHLOG
cashlog = []
def populate_cashlog():
    with open('cashlog.csv','rU') as h:
        reader = csv.reader(h)
        live = False
        for row in reader:
            if live:
                cashlog.append(LogLine(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            else:
                live = True
populate_cashlog()

sp500local = [logline.stock for logline in cashlog if logline.stock not in cashlog]

abc123 = {stock:0 for stock in sp500local}

#print abc123['KO']

stock_sets = [[]] #list of lists of LogLines/SplitObjs

def setup_stock_sets():
    curr = cashlog[0].stock
    for line in cashlog:
        if line.stock == curr:
            stock_sets[-1].append(line)
        elif line.stock != curr:
            stock_sets.append([line])
            curr = line.stock
    return None
setup_stock_sets()

class SplitObj(object):

    def __init__(self,dateline,stock,splitfrom,splitto):
        self.dateobj = Date(dateline)
        self.stock = stock
        self.splitfrom = float(splitfrom)
        self.splitto = float(splitto)

splitlines = []
def get_splits():
    with open('allsplitlines.csv','rU') as k:
        reader = csv.reader(k)
        for row in reader:
            splitlines.append(SplitObj(row[0],row[1],row[2],row[3]))
get_splits()
            
def intermix_splits(loglinelist,stock):
    mysplits = []
    for line in splitlines:
        if line.stock == stock:
            mysplits.append(line)
    out = mysplits + loglinelist
    out.sort(key = lambda r:r.dateobj.dateval)
    return out
    
currvals = {}
def getcurrvals(): 
    b = 'sp500currvals.csv'
    with open(b,'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] != 'N/A':
                currvals[row[0]] = float(row[1])
            else:
                currvals[row[0]] = row[1]
getcurrvals()

class ReportLine(object): #one for each closed position of each stock
                 
    def __init__(self,stock,totaldaysheld,cashmade,mostinvested,percentreturn,annualreturn):
        self.stock = stock
        self.totaldaysheld = totaldaysheld
        self.cashmade = cashmade
        self.mostinvested = mostinvested
        self.percentreturn = percentreturn
        self.annualreturn = annualreturn

endlog = []
def process_single(loglinelist):
    cleanlist = intermix_splits(loglinelist,loglinelist[0].stock)
    currpos = 0.0
    currshares = 0.0
    netcash = 0.0
    check = False
    netcashes = []
    a = Date('5/21/2015')
    aa = a.days_1jan1940()
    daysfrom1jan1940to21may2015 = aa
    for line in cleanlist:
        if check:
            if currpos == 0.0:
                pass
        if isinstance(line,SplitObj):
            currshares *= line.splitto/line.splitfrom
        elif isinstance(line,LogLine):
            if line.addsub == 'ADD':
                netcash += line.cashspentmade
                if line.amt > currpos:
                    currpos = 0.0
                else:
                    currpos -= line.amt
                currshares -= line.numshares
            elif line.addsub == 'SUB':
                currshares += line.numshares
                netcash -= line.cashspentmade
                currpos = line.amt
        check = True
        netcashes.append(netcash)
    selldate = loglinelist[-1].dateobj.days_1jan1940()
    if currpos > 0.0: #STILL HAVE SOME LEFT
        if currvals[line.stock] == 'N/A':
            return ReportLine(loglinelist[0].stock,held,netcash,(-1*min(netcashes)),("{}%".format((totalreturn)*100)),'n/a')
        else:
            netcash += currshares*currvals[line.stock]
            netcashes.append(netcash)
            selldate = daysfrom1jan1940to21may2015
        '''
        if currvals[line.stock] == 'N/A':
            endlog.append('N/A error')
        else:
            endlog.append(LogLine('ADD','5/21/15',line.stock,currvals[line.stock],currpos,currshares,(currvals[line.stock]*currshares),'x'))
        '''
    totalreturn = netcash/(-1*min(netcashes))
    held = selldate-loglinelist[0].dateobj.days_1jan1940()
    if held == 0:
        return ReportLine(loglinelist[0].stock,held,netcash,(-1*min(netcashes)),("{}%".format((totalreturn)*100)),'n/a')      
    else:
        return ReportLine(loglinelist[0].stock,held,netcash,(-1*min(netcashes)),("{}%".format((totalreturn)*100)),"{}%".format(totalreturn/held*365*100))      

def avg(lst):
    return sum(lst)/len(lst)
    
def process_all():
    out = []
    ###
    spans = []
    cashmades = []
    percreturns = []
    annreturns = []
    ###
    for lst in stock_sets:
        out.append(process_single(lst))
    with open('sp500report.csv','w') as b:
        writer = csv.writer(b)
        writer.writerow(['STOCK','DAYS HELD','CASH MADE/LOST','% RETURN','ANNUAL RETURN'])
        for rep in out:
            spans.append(rep.totaldaysheld)
            cashmades.append(rep.cashmade)
            percreturns.append(float(rep.percentreturn[:-1]))
            annreturns.append(float(rep.annualreturn[:-1]))
            writer.writerow([rep.stock,rep.totaldaysheld,rep.cashmade,rep.percentreturn,rep.annualreturn])
    print "*************"
    print "AVG TURNOVER: {} days".format(avg(spans))
    print "AVG PROFIT/LOSS: ${}".format(avg(cashmades))
    print "AVG PERC RETURN: {}%".format(avg(percreturns))
    print "AVG ANNUAL RETURN: {}%".format(avg(annreturns))
    print "*************"
process_all()



