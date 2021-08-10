
# modality keyword Search

Regex keyword search using input files

## config file
The config file contains a list of changeable parameters to suit your needs

 1. INCLUDE_UNMATCH_RESULTS
		 **a.** This parameter determines whether the code should output a second file with the the matched results only if this is false it will output the 2nd file under the filename specified in `["output-data"]["unmatched-data"]. If True it will do nothing.
 2. TEST_OR_PROD
	 **a.** This determines whether it should use the prod or test output and input listed in input-data and output-data
	 
 3. regex-file
	 **a.** This is the csv containing the regex file. It should have the regex followed by the category and subcategory you are looking to associate with the match.
	 
 4. regex-file-columns
	 **a.** This is used just to clarify the regex column names.
 5. input-data
	 **a.** This is to determine the input files for the script plus the column used to search for the regex.
 6. output-data
	 **a.** The output location for the main file and the optional matched only. (not names correctly)
	 
 7. analysis_data
	 **a.** The analysis location output. this is also printed at the end of the run time.
## General
The regex file doesnt have a good way of dealing with regex with no subcategories so i insert "None" in to these fields so that we can create a simple if statement in the code. So make sure that all empty fields in the regex definitions file has None instead (Can just `df.fillna()`) instead to get around this)




	

	 

	 
