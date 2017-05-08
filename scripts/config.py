from sqlalchemy import create_engine
import pandas as pd
from pyowm import OWM

user = str(input("Username: "))
pw = str(input("Password: "))
server = "192.168.0.111"
API_key = 'bd2cffa8775fb943b0de3d1a60d38fe5'
API_rate = 1.0 # Calls per second

engine = create_engine(
	"postgresql+psycopg2://" + user + ":" + pw + "@" + server 
	+ ":5432/WeatherWare",
	isolation_level = "AUTOCOMMIT")
	
con = engine.connect()

owm = OWM(API_key)

weatherColumns = [
	"city",
	"reception_time",
	"reference_time", 
	"clouds",
	"rain",
	"snow",
	"wind",
	"humidity",
	"pressure",
	"temp_min",
	"temp_max",
	"temp_morn",
	"temp_day",
	"temp_evening",
	"temp_night",
	"status",
	"detailed_status",
]

modelInputs = [
	"clouds", 
	"rain", 
	"wind", 
	"temp"
]

modelList = [
	"head", 
	"torso", 
	"legs", 
	"feet", 
	"accessories"
]