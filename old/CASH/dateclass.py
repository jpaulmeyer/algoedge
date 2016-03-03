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

        #self.dateval is what you sort on

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

def testdays1940():
    a = Date('1/6/00')
    b = Date('1/1/00')
    print a.days_1jan1940()-b.days_1jan1940()

testdays1940()

def testit():
    datestrings = ['1/1/01','12/31/94','10/11/54','12/1/00']
    for date in datestrings:
        a = Date(date)
        print "Datestring: {}\nM: {}\nD: {}\nY: {}\nDV: {}".format(a.meat,a.month,a.day,a.year,a.dateval)
    dates = [Date(elem) for elem in datestrings]
    dates.sort(key = lambda r:r.dateval)
    for date in dates:
        print date.dateval
    out = [elem.meat for elem in dates]
    return out
