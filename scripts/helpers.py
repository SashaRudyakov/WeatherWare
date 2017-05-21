from scriptConfig import *
from pandas.io import sql
import numbers

def pFormat(element):
	if (isinstance(element, int) or isinstance(element, float)
			or isinstance(element, numbers.Integral)):
		return(str(element))
	else:
		return("'" + str(element) + "'")

def desc(DataFrame):
	return(str(DataFrame.describe(include = "all")) + "\n")

def upsert(DataFrame, table, verbose = False, mode = "batch insert"):

	# Upserts DataFrame to table
	if verbose:
		print("Upserting to the '" + table + "' table:\n\n" + desc(DataFrame))

	# Batch insert mode
	if mode == "batch insert":
		DataFrame.to_sql(
				name = table,
				con = con,
				if_exists = "append",
				index = False
			)

	# Safe insert mode
	elif mode == "safe insert":
		dfLen = len(DataFrame.index)
		if dfLen > 10000:
			print("WARNING: This mode is VERY SLOW and you're userting "
				+ str(dfLen) + " records. Good luck!")
		for index, row in enumerate(np.array_split(DataFrame, dfLen)):
			try:
				row.to_sql(
					name = table,
					con = con,
					if_exists = "append",
					index = False
				)

			# Allow errors
			except Exception as error:
				if verbose:
					print("Row " + str(index) + " of " + table
						+ " hit the following error:\n" + str(error))
				pass

	# Update mode
	elif "update on " in mode:

		# Create PSQL update statement
		updateColumn = mode[10:]
		numUpdates = len(DataFrame[updateColumn])
		for curIndex in range(0, numUpdates):
			if verbose:
				print("Update " + str(curIndex + 1) + " of " + str(numUpdates)+ ":")

			# Create PSQL query
			updateStr = ("UPDATE " + table + " SET "
				+ ", ".join([colName + " = " + pFormat(DataFrame[colName][curIndex])
					for colName in list(DataFrame)])
				+ " WHERE " + updateColumn + " = " + pFormat(DataFrame[updateColumn][0])
					+ ";")
			if verbose:
				print(updateStr)
			sql.execute(updateStr, engine)

	# Unsupported mode parameter
	else:
		raise Exception("Unsupported mode: " + str(mode)
			+ ". Please select 'batch insert', 'safe insert', or 'update'.")

def download(columns = ["*"], table = None, where = None, verbose = False):

	# Create PSQL query
	assert table is not None, "Please specify a table."
	columns = ", ".join(columns)
	sql = "select " + columns + " from " + table
	if where is not None:
		sql += " where " + where + ";"
	else:
		sql += ";"

	# Read in as DataFrame
	if verbose:
		print("Executing:\n" + sql + "\n")
	DataFrame = pd.read_sql_query(sql = sql, con = con)
	if verbose:
		print(desc(DataFrame))
	return(DataFrame)

def updatePersonStats(user, stat):

	# Initialize variables
	willUpdate = False
	updateColumns = [
		"username",
		"last_" + stat + "_date",
		"days_" + stat + "_in_a_row",
		"days_" + stat + "_total"]

	# Get data
	personData = download(
		columns = updateColumns,
		table = "person",
		where = "username = " + pFormat(user))

	# If they "stat" yesterday
	if personData["last_" + stat + "_date"][0] == date.today() - timedelta(1):
		willUpdate = True
		newPersonData = pd.DataFrame(
			[[
				personData["username"][0],
				date.today(),
				personData["days_" + stat + "_in_a_row"][0] + 1,
				personData["days_" + stat + "_total"][0] + 1
			]],
			columns = updateColumns)

	# If it's been more than a day since they've "stat"
	elif personData["last_" + stat + "_date"][0] != date.today():
		willUpdate = True
		newPersonData = pd.DataFrame(
			[[
				personData["username"][0],
				date.today(),
				1,
				personData["days_" + stat + "_total"][0] + 1
			]],
			columns = updateColumns)

	# If the stats need to be updated
	if willUpdate:
		upsert(
			DataFrame = newPersonData,
			table = "person",
			verbose = True,
			mode = "update on username")
