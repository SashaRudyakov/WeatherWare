from flask import Flask, render_template, request, session, flash, redirect, url_for
import urllib2
import json
import sys

sys.path.append(sys.path[0][:-6] + "scripts")
from predict import *

# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)

app = Flask(__name__)

# Set "homepage" to index.html
@app.route('/')
def index():
    city = location['city']
    country = location['country_code']
    search = city + ", " + country
    prediction = predictClothes(search)
    weatherDict = getWeatherFromDB(search).to_dict('list')
    weather = dict([(i, weatherDict[i][0]) for i in weatherDict])
    return render_template('weather.html', location=search, prediction=prediction, weather=weather)

@app.route('/getPrediction', methods=['POST'])
def getPrediction():
    city = request.form['city']
    prediction = predictClothes(city)
    weatherDict = getWeatherFromDB(city).to_dict('list');
    weather = dict([(i, weatherDict[i][0]) for i in weatherDict])
    return render_template('weather.html', location=city,  prediction=prediction, weather=weather)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    session['logged_in'] = True
    session['username'] = username
    print(session)
    flash('You were logged in')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()
