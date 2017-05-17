from helpers import *
import holidays
import random
from predict import getWeatherFromDB

def getDailyMessages(user = None, city = None, numResults = 2):

	# Init the guaranteed list
	messageList = []

	# Init the potential list
	maybeList = [
		"You look swell today!",
		'"Rats! Rats! Everywhere ya look! Everywhere ya look there\'s '
			+ 'rats!"'' - Die Antwoord',
		"\"I've been to the Leaning Tower of Pisa. It's a tower, and it's "
			+ "leaning. You look at it, but nothing happens, so then you "
			+ "look for someplace to get a sandwich.\" - Danny DeVito",
		"Today might be a banking holiday somewhere. The more you know!"
	]

	# Holiday messages
	if city is None or city[-2:] == "US":
		curHoliday = holidays.UnitedStates().get(datetime.date.today())
		if curHoliday is not None:
			messageList = ["Happy " + curHoliday + "!"] + messageList

	# Other date messages
	curDate = str(datetime.date.today())[-5:]
	if curDate == "02-05":
		messageList = ["Happy anniversary, hunny!"
			] + messageList
	elif curDate == "03-14":
		messageList = ["Happy Pi Day, a holiday so important it's hard-coded!"
			] + messageList
	elif curDate == "04-10":
		messageList = ["Happy birthday to your friendly front-end developer, Sasha!"
			] + messageList
	elif curDate == "04-20":
		messageList = ["What, did you expect a special message today or something?"
			] + messageList
	elif curDate == "09-09":
		messageList = ["Happy birthday to your friendly back-end developer, Gaven!"
			] + messageList

	# Special user messages
	if user is not None:

		# Download user data
		personData = download(
			table = "person",
			where = "username = '" + user + "'")

		# Special username messages
		if "gaven" in user.lower() or "sasha" in user.lower():
			maybeList += ["I love your name, " + user + "!"]
		else:
			maybeList += ["What a swell name, " + user + "!"]

		# Days visited total messages
		if personData["days_visited_total"][0] == 1:
			messageList = ["Thank you so much for signing up!",
				"Make sure to give us feedback, that how our algorithms imporove!"
				] + messageList

		# Days visited in a row messages
		if personData["days_visited_in_a_row"][0] == 7:
			messageList = ["You've visited our website every day for a week! Go you!"
				] + messageList

		# Days suggested total messages
		if personData["days_suggested_total"][0] == 1:
			messageList = ["Thank you so much for giving us feedback!",
				"The more feedback you give us, the more we can tailor our "
				+ "suggestions to match your preferences!"] + messageList

		# Days suggested in a row messages
		if personData["days_suggested_in_a_row"][0] == 7:
			messageList = ["Holy moly, you're on a feedback streak! Keep it up!"
				] + messageList

	# Special city messages
	if city is not None:
		if city == "Boston, US":
			maybeList += ["What a swell city!"]

		# Give weather-based messages
		try:
			curWeather = getWeatherFromDB(city)["detailed_status"][0]
			if curWeather in ("heavy intensity rain", "moderate rain"):
				messageList += ["Have a good day, despite the rain!"]
			elif curWeather == "sky is clear":
				messageList += ["Looks like a beautiful day! Enjoy the sun!"]
		except:
			pass

	# Add maybeList to messageList if it's small
	if len(messageList) < numResults:
		messageList += random.sample(maybeList, min(len(maybeList),
			(numResults - len(messageList))))

	return(messageList)

# print(getDailyMessages())
# print(getDailyMessages("Gaven"))
# print(getDailyMessages(city = "Boston, US"))
