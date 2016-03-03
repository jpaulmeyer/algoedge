import plotly.plotly as py
from plotly.graph_objs import *
import requests
requests.packages.urllib3.disable_warnings()

from datetime import datetime







x1=['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00']
x2=['2013-10-06 22:23:00', '2013-11-06 22:23:00', '2013-12-06 22:23:00']
y1=[45.5,51.5,60]
y2=[40,35.5,47.1]




data = Data([  Scatter(x=x1,y=y1,name="Derp1"), Scatter(x=x2,y=y2,name="Derp2")  ])

layout = Layout(xaxis = XAxis(range = [\
    '2013-10-24 22:23:00','2013-12-04 22:23:00']))
fig = Figure(data=data,layout=layout)


plot_url = py.plot(fig, filename='JPaul\'s Graph!')
