#tracker.py

from calendarplay import *
from lookup import *
import plotly.plotly as py
from plotly.graphobjs import *


def pricetrack(sdate,edate,ticker): #or sid in place of ticker
    days = days_from_to(sdate,edate)
    xs1 = days
    ys1 = []
    for day in days:
        ys1.append(price_on_date(ticker,day))
    trace0 = Scatter(
        x = xs1,
        y = ys1,
        mode = 'lines',
        name = 'Price of ' + ticker,
        line = Line(
            color = 'rgb(255,0,0)',
            width = 2
        )
    )
    data = Data([trace0])
    plot_url = py.plot(data, filename='pricetrack('+ticker+')')

def innotrack(sdate,edate,ticker):
    days = days_from_to(sdate,edate)
    xs1 = days
    xs2 = []
    ys1 = []
    ys2 = []
    ylabels = []
    for day in days:
        ys1.append(price_on_date(ticker,day))
        inno = innovest_on_date(ticker,day)
        out = decide(inno,'main')
        if out[0] != 'none':
            xs2.append(day)
            ys2.append(inno.price) #or price_on_date(ticker,day)
            ylabels.append('{} {}'.format(out[0],str(out[1])))
    trace0 = Scatter(
        x = xs1,
        y = ys1,
        mode = 'lines',
        name = 'Price of ' + ticker,
        line = Line(
            color = 'rgb(255,0,0)',
            width = 2
        )
    )
    trace1 = Scatter(
        x = xs2,
        y = ys2,
        mode = 'markers',
        name = 'Innovest B/S Recs',
        marker = Marker(
            color = 'rgb(0,150,23)',
            size = 8
        )
    )
    data = Data([trace0, trace1])
    plot_url = py.plot(data, filename='innotrack('+ticker+')')
    
    
