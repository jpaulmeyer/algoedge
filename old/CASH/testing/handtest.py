import ystockquote

initcash = 10000000.0
cash = initcash
#a position is 100,000
p = 100000.0
stocks = {}





#AA - splits checked
'''
cash -= p/2 #BUY 0.5
stocks['AA'] = [.5,50000/57.31]

stocks['AA'][1] *= 2 # 2 for 1 split

cash -= p/2 #BUY +0.5
stocks['AA'][0] = 1.0
stocks['AA'][1] += 50000/26.6

cash -= p #BUY +1.0
stocks['AA'][0] = 2.0
stocks['AA'][1] += 100000/11.33

cash += stocks['AA'][1]*16.6/2.0 #SELL -1.0
stocks['AA'][0] = 1.0
stocks['AA'][1] /= 2.0

finalAA = 16.07                             #ystockquote.get_price('AA')
cash += 100000/finalAA #SELL REST
stocks['AA'] = [0,0]
'''
#AAPL - splits checked

print cash

#7/1/97
cash -= p #BUY 1.0
stocks['AAPL'] = [1.0,p/13.19]

print cash

#9/1/99
cash += (stocks['AAPL'][1]/2)*68.63 #SELL -0.5
stocks['AAPL'] = [.5,stocks['AAPL'][1]/2]

print cash

#9/2/99
cash += stocks['AAPL'][1]*70.56  #SELL REST
stocks['AAPL'] = [0,0]

#SPLIT 2 for 1 on 6/21/00
stocks['AAPL'][1] *= 2

#7/19/02
cash -= p/2 #BUY 0.5
stocks['AAPL'] = [.5,(p/2)/14.96]

print cash

#10/6/04
cash += stocks['AAPL'][1]*40.64 #SELL REST
stocks['AAPL'] = [0,0]

finalAAPL = 118.63 #ystockquote.get_price('AAPL')
#cash += 100000/finalAAPL

print "PROFIT: {}% in {} yrs".format((cash-initcash)/initcash*100,7)
print cash

########
'''
NOT DONE: Need to sell half of a position and make sure its right amt.
Finish tracing this all out then test!!!

- Whenever you sell last half, sell all remaining shares.
'''
########
