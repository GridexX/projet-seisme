#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from libcomcat.search import search
from datetime import datetime,timedelta

app = Flask(__name__)


def lastseismes(eventlist):
    
    n = len(eventlist)  
    listseismes = list()

    for x in range(n):
        event = eventlist[x]       
        listseismes.append(dict())
        listseismes[x]["location"] = event.location
        listseismes[x]["magnitude"] = event.magnitude
        listseismes[x]["latitude"] = event.latitude
        listseismes[x]["longitude"] = event.longitude
        listseismes[x]["time"] = "".join(list(str(event.time))[0:19])
        listseismes[x]["depth"] = event.depth
        listseismes[x]["url"] = event.url
    
    return listseismes



@app.route('/')
@app.route('/template')
@app.route('/seismes')
@app.route('/map')
def jinja():
    date_now = datetime.now()
    date_last_minute = datetime.now() - timedelta(hours=5)
    eventlist = search(starttime=date_last_minute,
                       endtime=date_now,
                       minmagnitude=0)

    listseismes = lastseismes(eventlist)
    return render_template('map_v2_1.html', listseismes=listseismes)


@app.route('/lastseismes')
@app.route('/lastseismes/<int:num_page>')
def seismes(num_page=5):
    date_now = datetime.now()
    date_last_minute = datetime.now() - timedelta(hours=num_page)
    eventlist = search(starttime=date_last_minute,
                       endtime=date_now,
                       minmagnitude=0)

    listseismes = lastseismes(eventlist)
    return render_template('map_v2_1.html', listseismes=listseismes)


if __name__ == '__main__':
    app.run(debug=True)
