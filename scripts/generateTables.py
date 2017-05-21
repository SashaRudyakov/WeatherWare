from helpers import *
import itertools
import csv
from predict import createModels

# To start server:
# pg_ctl -D E:\WeatherWareDB start

# Generate cities table
reg = owm.city_id_registry()
reg = [line.split(',') for line in reg._get_all_lines()]
countryList = []
for line in reg:
	try:
		countryList += [[
			line[0],
			int(line[1]),
			float(line[2]),
			float(line[3]),
			line[4][0:2]
		]]
	except:
		print("ERROR: " + str(line))
reg = pd.DataFrame(countryList, columns = [
	'city_name',
	'city_id',
	'latitude',
	'longitude',
	'country'])
upsert(reg, 'cities', verbose = True)

# Generate clothing table
clothes = pd.DataFrame(
	[
		["Head", "Nothing"],
		["Head", "Baseball Cap or Sunglasses"],
		["Head", "Winter Hat"],
		["Head", "Winter Hat and Scarf"],

		["Torso", "T-Shirt"],
		["Torso", "Long Sleeve Shirt"],
		["Torso", "Sweatshirt"],
		["Torso", "Jacket"],
		["Torso", "Winter Coat"],
		["Torso", "Raincoat"],

		["Legs", "Shorts"],
		["Legs", "Pants"],
		["Legs", "Heavy Pants"],

		["Feet", "Sandals"],
		["Feet", "Shoes"],
		["Feet", "Boots"],

		["Accessories", "Nothing"],
		["Accessories", "Umbrella"],
	],
	columns = ['slot', 'item'])
upsert(clothes, 'clothes', verbose = True)

# Create training set
optionsList = [
	[user], # username
	[0, 25, 50, 75, 100], # clouds
	[0, 10, 50], # rain
	[0, 1], # snow
	[0, 5, 10], # wind
	[20, 40, 50, 60, 70, 85] # temp
]
with open("scripts" + delim + "trainingSet.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(list(itertools.product(*optionsList)))
trainingSet = pd.read_csv("scripts" + delim + "trainingSetWithOutput.csv")
upsert(trainingSet, 'training_set', verbose = True)
createModels(verbose = True)
