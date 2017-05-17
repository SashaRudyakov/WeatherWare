from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pyowm import OWM
import itertools
import getpass
import platform
import pickle
import datetime

# If you've already gone through setup
fileLocation = "localData.pkl"
try:
	pkl_file = open(fileLocation, 'rb')
	user, pw, server, API_key, hash_key = pickle.load(pkl_file)

# If not, prompt user to fill it out
except:
	print("Commencing first time setup:")
	pkl_file = open(fileLocation, 'wb')
	user = raw_input("PSQL Username:\t")
	pw = getpass.getpass("PSQL Password:\t")
	server = raw_input("PSQL Server IP:\t")
	API_key = raw_input("OWM API Key:\t")
	hash_key = getpass.getpass("AES Key:\t")
	pickle.dump([user, pw, server, API_key, hash_key], pkl_file)

# DB info
engine = create_engine(
	"postgresql+psycopg2://" + user + ":" + pw + "@" + server
	+ ":5432/WeatherWare",
	isolation_level = "AUTOCOMMIT")
con = engine.connect()

# Because Windows file paths are stupid
if platform.system() == "Windows":
	delim = "\\"
else:
	delim = "/"

# API info
API_rate = 1.0 # Calls per second
owm = OWM(API_key)

# All weather attributes from API
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

# Weather attributes currently used in predictions
modelInputs = [
	"clouds",
	"rain",
	"snow",
	"wind",
	"temp"
]

# What's being predicted from models
modelList = [
	"head",
	"torso",
	"legs",
	"feet",
	"accessories"
]

# Columns in person table
personColumns = itertools.product(
	modelList,
	modelInputs,
	["mult", "add"])
daysColumns = itertools.product(
	["days"],
	["visited", "suggested"],
	["total", "in_a_row"])
personColumns = (["username", "pw", "last_visit", "last_suggestion"]
	+ ["_".join(column) for column in daysColumns]
	+ ["_".join(column) for column in personColumns])
