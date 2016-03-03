from urllib2 import urlopen
import csv

currvals = {}

print "*******\nThis program first gets you your currvals to sell" + \
    "out at in STEP 1...\nThen you correct that csv in STEP 2...\n" + \
    "Then you get a new bigfile with a real start and end date in STEP 3!\n******"

def getcurrvals_bydate(month,day,year):
    month2 = None
    day2 = None
    year2 = None
    if month > 12 or month < 1 or day < 1 or day > 31 or year < 1994:
        return "ERROR invalid input"
    if month == 1 and day == 1:
        month2 = 12
        day2 = 31
        year2 = year-1
    elif day == 1 and month != 1:
        month2 = month - 1
        if month2 in [1,3,5,7,8,9,12]:
            day2 = 31
        elif month2 in [4,6,10,11]:
            day2 = 30
        else:
            day2 = 28
        year2 = year
    else:
        day2 = day - 1
        month2 = month
        year2 = year
        
    url = "http://54.69.46.205/filter_csv.php?sdate={}/{}/{}&eda".format(month2,day2,year2) + \
        "te={}/{}/{}&pid=9".format(month,day,year)
    return url

print "STEP 1 - End Date"
a = int(raw_input("MONTH: "))
b = int(raw_input("DAY: "))
c = int(raw_input("YEAR: "))

print "USE THIS URL: \n"
print getcurrvals_bydate(a,b,c)
e = raw_input("****\nready to proceed????\n****\n")

print "STEP 2 - Fix CSV"
def fix_csv(filenum):
    temp = []
    print "Make sure they're in the same directory! (Using file-{} as filename)".format(filenum)
    with open('file-{}.csv'.format(filenum), 'rU') as h:
        reader = csv.reader(h)
        for row in reader:
            temp.append([row[1],row[2]])

    with open('enddatevals.csv','w') as g:
        writer = csv.writer(g)
        live = False
        for row in temp:
            if live:
                writer.writerow([row[0],row[1]])
            else:
                live = True
            
print "Fixing csv, enter in filenum ('file-#')\n"
d = raw_input("Filenum? ")
fix_csv(d)

print "STEP 3 - Get lines to analyze..."
print "START DATE!"
f = int(raw_input("MONTH: "))
j = int(raw_input("DAY: "))
k = int(raw_input("YEAR: "))
def get_startendlines(smonth,sday,syear,knowhens):
    urls = []
    for knoval in knowhens:
        urls.append("http://54.69.46.205/filter_csv.php?sdate={}/{}/{}&eda".format(smonth,sday,syear) + \
            "te={}/{}/{}&knowhen={}&pid=9".format(a,b,c,knoval))
    for guy in urls:
        print guy
        print "\n\n"

print "NOW USE THESE URLS: \n"
get_startendlines(f,j,k,['311','313','415','417'])
raw_input("Ready to proceed again? ")
print "ARE ALL THOSE IN THE SAME DIR AND NAMED file-# ?"

def compile_csvs(nums):
    alllines = []
    for num in nums:
        with open("file-{}.csv".format(num,'rU')) as derp:
            reader = csv.reader(derp)
            for row in reader:
                alllines.append(row)

    with open('giantunsorted.csv','w') as herp:
        writer = csv.writer(herp)
        writer.writerow(["Date","Stock","KNO","W","H","E","N","RD","%"])
        for row in alllines:
            if row[0] != 'date':
                writer.writerow(row)

filenums = []
live = True
while live:
    tempo = raw_input("Enter a filenum, or 'done' if finished: ")
    if tempo == 'done':
        live = False
    else:
        filenums.append(tempo)
                    
compile_csvs(filenums)

print "\n\n\nall done"





