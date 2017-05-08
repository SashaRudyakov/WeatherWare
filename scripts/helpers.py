from config import *

def upsert(DataFrame, table, verbose = False):
	
	# Upserts DataFrame to table
	if verbose:
		print("Upserting to the '" + table + "' table:\n\n" 
			+ str(DataFrame.describe(include = "all")) + "\n")
	DataFrame.to_sql(
			name = table, 
			con = con, 
			if_exists = "append", 
			index = False
		)
		
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
		print(str(DataFrame.describe(include = "all")) + "\n")
	return(DataFrame)