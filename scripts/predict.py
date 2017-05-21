from helpers import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from datetime import datetime

def getWeatherFromDB(city, columns = ["*"], verbose = False):

	# Return most recent for that city
	dateStr = str(datetime.now().date())
	weather = download(
		columns = columns,
		table = "weather",
		where = "city = '" + city + "' and reference_time like '%%"
			+ dateStr + "%%' order by reception_time desc limit 1;",
		verbose = verbose)
	return(weather)

def createModels(models = modelList, verbose = False):

	# Download inputs/outputs
	weather = download(table = "training_set")
	clothing = weather[models]
	weather = weather[modelInputs]

	# Create models
	for model in models:
		try:
			if verbose:
				print("Creating " + model + " model...")
			clf = RandomForestClassifier(n_estimators = 10)
			clf = clf.fit(
				weather,
				clothing.query(model + " != ''")[model].values.ravel())
			joblib.dump(clf, "scripts" + delim + "models" + delim + model
				+ 'Model.pkl')
			if verbose:
				print("Done.")
		except Exception as error:
			print("\nCould not create the " + model + " model.\n"
				+ str(error) + "\n")

def applyModel(model, weather):
	return str(joblib.load("scripts" + delim + "models" + delim + model
		+ 'Model.pkl').predict(weather)[0])

def applyPreference(weather, model, person = None, verbose = False):

	# If person is None just return the weather
	if person is None:
		return(weather)

	# Else, apply preferences from person table
	try:
		print("YOU STILL NEED TO WRITE THIS")
		return(weather)

	# If model or person don't exist, just return weather
	except Exception as error:
		print("Could not apply preference for the following:\nWeather: "
			+ str(weather) + "\nModel: " + model + "\nPerson: " + str(person)
			+ "\nError: " + str(error))
		return(weather)


def predictClothes(city, models = modelList, person = None, verbose = False):

	# Get current weather
	curWeather = getWeatherFromDB(city, columns = modelInputs)
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
		createModels(verbose = verbose)
		prediction = {model: applyModel(model, perceivedWeather[model])
			for model in models}

	# Returns dict of clothing predictions
	if verbose:
		print("\nPrediction:\n" + str(prediction))
	return(prediction)

def giveSuggestion(suggestion, weather = None, city = None, user = None,
	verbose = False):

	# Update suggested stats
	if user is not None:
		updatePersonStats(user, "suggested")

	# Parameter handling
	if weather is None and city is None:
		raise Exception("When calling 'giveSuggestion', either 'weather' or "
			+ "'city' must be provided.")

	# If weather is not provided, get from DB
	elif weather is None:
		weather = getWeatherFromDB(
			columns = modelInputs,
			city = city)

	# Upsert weather with suggestions
	suggestionDF = pd.DataFrame(
		[
			[user]
			+ [weather[modelInput][0] for modelInput in modelInputs]
			+ suggestion.values()
		],
		columns = ["username"] + modelInputs + suggestion.keys())
	upsert(suggestionDF, 'training_set', verbose = verbose)

# # Example calls:
# print(getWeatherFromDB("Boston, US"))
# createModels(verbose = True)
# print(predictClothes("Boston, US", verbose = True))
# print(giveSuggestion({"head": "Nothing"}, city = "Boston, US"))
