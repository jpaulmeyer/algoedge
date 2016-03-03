#strategies.py

def strat0(kno,pct):
    if str(kno)[:2] == '41':
        if int(pct) == 83:
            return ('buy',0.5)
        elif int(pct) == 92:
            return ('buy',1.0)
        elif int(pct) == 100:
            return ('buy',2.0)
    elif str(kno)[:2] == '31':
        if int(pct) == 83:
            return ('sell',0.5)
        elif int(pct) == 92:
            return ('sell',1.0)
        elif int(pct) == 100:
            return ('sell',2.0)
    else:
        return ('none',0.0)

def decide(inno,stratkey):
    if stratkey == 'main':
        return strat0(inno.kno,inno.pct)
    else:
        print 'other strategies not yet implemented'


