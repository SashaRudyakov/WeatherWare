from helpers import *
import hashlib, binascii

def encrypt(string):
	return(binascii.hexlify(hashlib.pbkdf2_hmac('sha256', hash_key, string,
		100000)))

def signIn(user, pw):
	personData = download(
		columns = ["pw"],
		table = "person",
		where = "username = '" + user + "'")
	if len(personData["pw"]) == 0:
		return("User not found.")
	if personData["pw"][0] == encrypt(pw):
		return("Authentication successful.")
	else:
		return("Wrong password.")

def signUp(user, pw):

	# If you already signed up
	try:
		personData = download(
			columns = ["username"],
			table = "person",
			where = "username = '" + user + "'")
		if len(personData["username"]) != 0:
			return("Looks like you already have an account.")
	except:
		pass

	# Else, sign up
	signUpData = pd.DataFrame(
		[
			[user, encrypt(pw), datetime.date.today(), None]
			+ [1] * 2 + [0] * 2 + [1, 0] * ((len(personColumns) - 8) / 2)
		],
		columns = personColumns
	)
	upsert(signUpData, "person")
	return("You have been signed up for WeatherWare. Enjoy!")

# print(signUp("Gaven", pw))
# print(signUp("Gaven", "test"))
# print(signIn("Gaven", pw))
# print(signIn("Gaven", "test"))
# print(signIn("Sasha", "test"))
