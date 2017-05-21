from helpers import *
import hashlib, binascii

def encrypt(string):

	# Use sha256 hash for password encryption
	return(binascii.hexlify(hashlib.pbkdf2_hmac('sha256', hash_key, string,
		100000)))

def signIn(user, pw):

	# Download their data
	personData = download(
		columns = ["username", "pw"],
		table = "person",
		where = "username = " + pFormat(user))

	# If user is not found
	if len(personData["pw"]) == 0:
		return("User not found.")

	# If Authentication fails
	elif personData["pw"][0] != encrypt(pw):
		return("Wrong password.")

	# If authentication successful
	else:

		# Update visited stats
		updatePersonStats(user, "visited")

		# Return success
		return("Authentication successful.")

def signUp(user, pw):

	# If you already signed up
	try:
		personData = download(
			columns = ["username"],
			table = "person",
			where = "username = " + pFormat(user))
		if len(personData["username"]) != 0:
			return("Looks like you already have an account.")
	except:
		pass

	# Else, sign up
	signUpData = pd.DataFrame(
		[
			# To match structure of person table
			[user, encrypt(pw), date.today(), None]
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
