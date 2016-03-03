
# E D I T     H E R E
inputName = 'dadspfirst10.csv' #must exist already
currvalsName = 'sp500currvals.csv'
splitsName = 'allsplitlines.csv'
relogstocks = False
rescrapesplits = False

from logstocks import *
#LOG CURRENT VALUES (logstocks.py)
if relogstocks:
    logstocks(inputName,currvalsName,True,True,None)

from scraper import *
#SCRAPE STOCK SPLITS (scraper.py)
if rescrapesplits:
    populatestocks(currvalsName)
    scrapeallsplits(stockz9,splitsName) #uses currvals

#LINECLASS
from lineclass4 import *

#CASH5 BABY
from cash5 import *




    
