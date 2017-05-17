from helpers import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from datetime import datetime

def getWeatherFromDB(city, columns = ["*"], verbose = False):

	# Return most recent for that city
	dateStr = str(datetime.now().date())
	myData = download(
		columns = columns,
		table = "weather",
		where = "city = '" + city + "' and reference_time like '%%" 
			+ dateStr + "%%' order by reception_time desc limit 1;",
		verbose = verbose)
	return(myData)
	
def createModels(models = modelList, verbose = False):
	
	# Create model for each prediction
	for model in models:
	
		# Download input
		weather = download(
			columns = modelInputs,
			table = "training_set")
			
		# Download output
		clothing = download(
			columns = [model],
			table = "training_set")
			
		# Create model
		try:
			if verbose:
				print("Creating " + model + " model...")
			clf = RandomForestClassifier(n_estimators = 10)
			clf = clf.fit(weather, clothing.values.ravel())
			joblib.dump(clf, "scripts" + delim + "models" + delim + model 
				+ 'Model.pkl')
			if verbose:
				print("Done.")
		except Exception as error:
			print("\nCould not create the " + model + " model.\n" 
				+ str(error) + "\n")
			time.sleep(1)

def applyModel(model, weather):
	return str(joblib.load("scripts" + delim + "models" + delim + model 
		+ 'Model.pkl').predict(weather)[0])

def applyPreference(weather, model, person = None):
	
	# If person is None just return the weather
	if person is None:
		return(weather)

	# Else, apply preferences from person table
	try:
		print("YOU STILL NEED TO WRITE THIS")
		return(weather)

	# If model or person don't exist, just return weather
	except:
		print("Could not apply preference for the following:\nWeather: " 
			+ str(weather) + "\nModel: " + model + "\nPerson: " + str(person))
		return(weather)


def predictClothes(city, models = modelList, person = None, verbose = False):
	
	# Get current weather
	curWeather = getWeatherFromDB(city, 
		columns = ["clouds", "rain", "wind", "temp_day"])
	if verbose:
		print("Current weather in " + city + ":\n" + str(curWeather))

	# Get perceived weather for each model
	perceivedWeather = {model: applyPreference(curWeather, model, person) 
		for model in models}
	
	# Apply each model
	try:
		prediction = {model: applyModel(model, perceivedWeather[model]) 
			for model in models}

	# If models don't exist, make them	
	except:
		createModels()
		prediction = {model: applyModel(model, perceivedWeather[model]) 
			for model in models}

	# Returns dict of clothing predictions
	if verbose:
		print("\nPrediction:\n" + str(prediction))
	return(prediction)

# # Example calls:
# print(getWeatherFromDB("Boston, US"))
# createModels(verbose = True)
# predictClothes("Boston, US", verbose = True)
