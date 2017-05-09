from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import urllib2
import json

# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
print(location);

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://192.168.0.111:5432/WeatherWare?user=gaven_000&password=penhouse873&ssl=true'
db = SQLAlchemy(app)

# Create our database model
#class User(db.Model):
#    __tablename__ = "users"
#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(120), unique=True)

#    def __init__(self, email):
#        self.email = email

#    def __repr__(self):
#        return '<E-mail %r>' % self.email

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Weather
@app.route('/weather')
def weather():
    db.session.query('select count(*) from cities')   
    return render_template('location.html', location=location)

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
