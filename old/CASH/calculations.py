def annualreturn(initial,final,years):
    return str((((float(final)/float(initial))**(1./years))-1)*100)[:6] + " %"

print "ME"
print annualreturn(1000,5700,14)
print "SP500"
print annualreturn(1000,2282,14)
