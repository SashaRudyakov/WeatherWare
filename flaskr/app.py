from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import urllib2
import json
import sys

sys.path.insert(0, '/Users/sasharudyakov/Development/WeatherWare/flaskr/scripts')
from predict import *

# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
print(location);

app = Flask(__name__)

# Set "homepage" to index.html
@app.route('/')
def index():
    city = location['city']
    country = location['country_code']
    search = city + ", " + country
    prediction = predictClothes(search)
#    weather = dict([(key, value[0]) for key, value in getWeatherFromDB(search).to_dict('list')]);
    weather = getWeatherFromDB(search).to_dict('list');
    return render_template('cool.html', location=search, prediction=prediction, weather=weather)

@app.route('/getPrediction', methods=['POST'])
def getPrediction():
    city = request.form['city']
    prediction = predictClothes(city)
#    weather = dict([(key, value[0]) for key, value in getWeatherFromDB(city).to_dict('list')]);
    weather = getWeatherFromDB(city).to_dict('list');
    return render_template('cool.html', location=city,  prediction=prediction, weather=weather)

# Weather
#@app.route('/weather')
#def weather():
#    db.session.query('select count(*) from cities')   
#    return render_template('location.html', location=location)
if __name__ == '__main__':
    app.debug = True
    app.run()
