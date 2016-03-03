from calendar import Calendar
from datetime import date

#Helper function for days_of
def find_start_num(year):
    firsts = []
    for i in range(7):
        firsts.append(Calendar(i).yeardatescalendar(year)[0][0][0][0])
    for elem in firsts:
        if elem.day == 1:
            return firsts.index(elem)
    return -1 #error

#Turns arguments of function into a datestring
def dateify1(year,month,day):
    #yyyy-mm-dd
    outmonth = -1
    outyear = -1
    outday = -1
    if len(str(month)) == 2:
        outmonth = str(month)
    else:
        outmonth = '0' + str(month)
    if len(str(day)) == 2:
        outday = str(day)
    else:
        outday = '0' + str(day)
    return str(year) + '-' + outmonth + '-' + outday

#Returns the days of the year 1996 etc. as lst days w/in lst months w/in lst yrs
def days_of(startyear,endyear,dateasstring=True):
    allthedays = []
    for year in range(startyear,endyear):
        lstyear = []
        for month in range(1,13):
            months = Calendar(find_start_num(year)).itermonthdays(year,month)
            lstmonth = []
            for day in months:
                lstmonth.append(dateify1(year,month,day))
            cleanlstmonth = []
            for daystring in lstmonth:
                if daystring[-3:] != '-00':
                    cleanlstmonth.append(daystring)
            lstyear.append(cleanlstmonth)
        allthedays.append(lstyear)
    outall = []
    if not dateasstring:
        for year in allthedays:
            outyear = []
            for month in year:
                outmonth = []
                for day in month:
                    outmonth.append(date(int(day[:4]),int(day[5:7]),int(day[8:])))
                outyear.append(outmonth)
            outall.append(outyear)
    if dateasstring:
        return allthedays
    elif not dateasstring:
        return outall

#Takes output of days_of and flattens into one list to make more simple
def onelist(daysof):
    out = []
    for year in daysof:
        for month in year:
            for day in month:
                out.append(day)
    return out

#Returns lst of days up to a certain datestring?
def days_up_to(date,dateasstring,endyr):#end
    end = []
    fullend = onelist(days_of(endyr,endyr+1,dateasstring))
    live = True
    for day in fullend:
        if live:
            end.append(day)
        if day == date:
            live = False
    return end

def days_after(date,dateasstring,startyr):#start
    start = []
    fullstart = onelist(days_of(startyr,startyr+1,dateasstring))
    live = False
    for day in fullstart:
        if live:
            start.append(day)
        elif day == date:
            live = True
            start.append(day)
    return start

#Takes in 2 datetime objects
def days_from_to(start,end,dateasstring=False): #inclusive
    if end < start:
        print "ERROR: End date must be equal to or after start date"
        return
    startyr = start.year
    endyr = end.year
    diff = endyr - startyr
    if diff == 0:
        a = days_up_to(end,dateasstring,startyr)
        b = days_after(start,dateasstring,startyr)
        return [val for val in a if val in b]
    elif diff == 1:
        return days_after(start,dateasstring,startyr) + days_up_to(end,dateasstring,endyr)
    elif diff > 1:
        middle = onelist(days_of(startyr+1,endyr,dateasstring))
        start = days_after(start,dateasstring,startyr)
        end = days_up_to(end,dateasstring,endyr)
        return start + middle + end


c = days_from_to(date(2000,1,6),date(2000,6,12))
if __name__ == '__main__':
    print c


        
