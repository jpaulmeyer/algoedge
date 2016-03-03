#stockuniverses.py

#SP500
#DOW
#IB or whatever etc
#Russell 2k

def getuniverse(univkey):
    if univkey == 'testuniv':
        return ['AA','AAPL','AKAM','KO']
    else:
        print 'not implemented'
        return ['AAPL']
