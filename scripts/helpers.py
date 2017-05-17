from scriptConfig import *

def desc(DataFrame):
	return(str(DataFrame.describe(include = "all")) + "\n")

def upsert(DataFrame, table, verbose = False, mode = "batch"):
	
	# Upserts DataFrame to table
	if verbose:
		print("Upserting to the '" + table + "' table:\n\n" + desc(DataFrame))

	# Batch mode
	if mode == "batch":
		DataFrame.to_sql(
				name = table, 
				con = con, 
				if_exists = "append", 
				index = False
			)

	# Safe mode
	elif mode == "safe":
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

	# Unsupported mode parameter
	else:
		raise Exception("Unsupported mode: " + str(mode) 
			+ ". Please select either 'batch' or 'safe'.")
		
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