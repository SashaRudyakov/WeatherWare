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
				print("Starting " + model + " model...")
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

def predictClothes(city, models = modelList, verbose = False):
	
	# Get current weather
	curWeather = getWeatherFromDB(city, 
		columns = ["clouds", "rain", "wind", "temp_day"])
	if verbose:
		print("Current weather in " + city + ":\n" + str(curWeather))
	
	# Apply each model
	prediction = {model: str(joblib.load("scripts" + delim + "models" + delim 
		+ model + 'Model.pkl').predict(curWeather)[0]) for model in models}
	if verbose:
		print("\nPrediction:\n" + str(prediction))
	return(prediction)

# # Example calls:
# print(getWeatherFromDB("Boston, US"))
# createModels(verbose = True)
# predictClothes("Boston, US", verbose = True)
