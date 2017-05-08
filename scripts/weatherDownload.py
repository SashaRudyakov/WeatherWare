from helpers import *
import time
import sys

def weatherToDF(weather, location, forecast, unit = "fahrenheit"):
	
	# Converts weather object into a single row DataFrame
	return(pd.DataFrame(
		[[
			location,
			forecast.get_reception_time(timeformat = 'iso'),
			weather.get_reference_time(timeformat = 'iso'),
			weather.get_clouds(),
			weather.get_rain().get('all', 0),
			weather.get_snow().get('all', 0),
			weather.get_wind().get('speed', 0),
			weather.get_humidity(),
			weather.get_pressure().get('press', None),
			weather.get_temperature(unit = unit).get(u'min', None),
			weather.get_temperature(unit = unit).get(u'max', None),
			weather.get_temperature(unit = unit).get(u'morn', None),
			weather.get_temperature(unit = unit).get(u'day', None),
			weather.get_temperature(unit = unit).get(u'eve', None),
			weather.get_temperature(unit = unit).get(u'night', None),
			weather.get_status(),
			weather.get_detailed_status()
		]],
		columns = weatherColumns
	))
	
def upsertCityWeather(city, limit = 16, verbose = False, retries = 3):
	
	# Get forecast for the city
	getWeatherSuccess = False
	for attempt in range(retries):
		if not getWeatherSuccess:
			try:
				forecast = owm.daily_forecast(city, limit = limit
					).get_forecast()
				getWeatherSuccess = True
			except Exception as error:
				print("\nERROR GETTING WEATHER: " + city + "\n" 
					+ str(error) + "\n")
				time.sleep(1)
	
	# Else, exit
	if not getWeatherSuccess:
		print("Unable to get weather for " + city + ".")
		return None
	
	# Make list of DataFrames
	weathers = [weatherToDF(
		weather = weather, 
		location = city, 
		forecast = forecast
	) for weather in forecast]
	
	# Combine into one DataFrame
	readyToUpsert = pd.DataFrame()
	for weather in weathers:
		readyToUpsert = readyToUpsert.append(weather)
	if verbose:
		print("Upserting weather for " + city + ":\n\n"
			+ str(readyToUpsert.describe(include = "all")) + "\n")
	
	# Upsert the combined DataFrame
	upsertSuccess = False
	for attempt in range(retries):
		if not upsertSuccess:
			try:
				upsert(DataFrame = readyToUpsert, table = 'weather')
				upsertSuccess = True
			except Exception as error:
				print("\nERROR UPSERTING WEATHER: " + city + "\n" 
					+ str(error) + "\n")
				time.sleep(1)

def upsertCountryWeather(country, limit = 16, verbose = False, retries = 3,
		startIndex = 0, printUpdatesPerMinute = 1):

	# Get unique cities
	cities = download(
		columns = ["city_name", "country"], 
		table = "cities", 
		where = "country = '" + country + "'", 
		verbose = True)
	cities = cities.drop_duplicates().reset_index(drop = True)
	print("After de-duping:\n\n" + str(cities.describe(include = "all")) + "\n")

	# Loop through cities
	startTime = time.time()
	curIndex = startIndex
	for index, row in cities.iterrows():
		if index > startIndex:
			try:
				curIndex += 1
				curTime = time.time()
				curCity = str(row["city_name"]) + ", " + str(row["country"])
				
				# Print updates logic
				if verbose or curIndex == startIndex + 1 or (
						printUpdatesPerMinute is not None
						and printUpdatesPerMinute != 0
						and curIndex % round(API_rate * 60.0 
							/ printUpdatesPerMinute) == 0):
					print("Getting city " + str(curIndex) + ": " + curCity 
						+ "...")
				
				# Upsert
				try:
					upsertCityWeather(
						city = curCity, 
						limit = limit, 
						verbose = False, 
						retries = retries)
				except Exception as error:
					print("\nERROR: " + curCity + "\n" + str(error) + "\n")
				
				# Sleep logic
				time.sleep(max(0, ((curIndex - startIndex) 
					- (curTime - startTime)) / API_rate))
					
			# Seems like it's due to unicode characters showing up
			except Exception as error:
				print("\nUNKNOWN ERROR AT INDEX " + str(curIndex) + ":\n" 
					+ str(error) + "\n")

# If called directly, keep refreshing US data
if __name__ == "__main__":
	while True:
		upsertCountryWeather(country = "US")