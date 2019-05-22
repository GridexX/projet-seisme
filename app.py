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
@app.route('/lastseismes')
@app.route('/lastseismes/<int:num_page>')
@app.route('/lastseismes/<int:num_page>/<int:refresh>')
def seismes(num_page=5, refresh=1):
    date_now = datetime.now()
    date_last_hour= date_now - timedelta(hours = num_page)

    eventlist = search(starttime = date_last_hour,
                       endtime = date_now,
                       minmagnitude = 0)

    listseismes = lastseismes(eventlist)
    lenlist = len(listseismes)
    return render_template('map_v2_1.html', listseismes=listseismes, refresh=refresh, lenlist=lenlist)


@app.route('/lastseismes_v2/<int:date_format>/')
@app.route('/lastseismes_v2/<int:date_format>/<int:refresh>')
def seismes_v2(date_format, refresh=1):
    date_now = datetime.now()
    if date_format == 0:
        date_past= date_now - timedelta(hours = date_now.hour)
    elif date_format == 1:
        date_past = date_now - timedelta(days = date_now.weekday())
    elif date_format == 2:
        date_past = date_now - timedelta(days = date_now.day)

    eventlist = search(starttime = date_past,
                       endtime = date_now,
                       minmagnitude = 0)

    listseismes = lastseismes(eventlist)
    lenlist = len(listseismes)
    return render_template('map_v2_1.html', listseismes=listseismes, refresh=refresh, lenlist=lenlist)


@app.route('/equipe')
def equipe():
    return render_template('equipe_v2.html')


if __name__ == '__main__':
    app.run(debug=True)
