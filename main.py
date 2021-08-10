from os import sep
import pandas as pd 
import re
import yaml
import math
# from test import autotest

category_keyword_count = {}
subcat_keyword_count = {}


def keyword_analysis_dictionary(field, dictionary_name):
    ''' Takes in the field and adds it or increments it to the global dictionary of cat or sub cat
        This will provide a count of the unique categors and sub categorys matched.    
    '''
    if dictionary_name == "subcat":
        dictionary = subcat_keyword_count
    elif dictionary_name == "cat":
        dictionary = category_keyword_count
    if field in dictionary:
        dictionary[field] += 1
    else:
        dictionary[field] = 1


def run_regex_search(input_data, regex_file):
    """
        Runs a regex search over a singular column, constructs an array of array of matches and then appends this
        to the final dataframe. 
    """
    # Storage of the final columns to add to the dataframe
    category = []
    subcategory = []
    regex_output = []

    # This is to print progress of script by outputing every 5% complete
    row_count = len(input_data.index)
    print("starting for loop")
    for index_output, row_output in input_data.iterrows():
        # To output progress of script
        if index_output % int((row_count/100)*5) == 0 and index_output != 0:
            print(f"{int(((index_output+1)/row_count)*100)}%")
        # Temp holders of the arrays matched
        temp_category = []
        temp_sub_category = []
        temp_regex = []

        for index_regex, row_regex in regex_file.iterrows():
            regex = row_regex[config["regex-file-columns"]["regex"]]
            content = row_output[config["input-data"]["column-to-search"]]
            # If the input data file has empty fields handle it by skiping iteration
            if not isinstance(content, str):
                continue
            # If match the regex
            if re.search(regex, content, re.IGNORECASE):
                temp_regex.append(regex)
                if not row_regex[config["regex-file-columns"]["regex"]] == "None":
                    # if the subcat is already in the array dont append again
                    if not row_regex[config["regex-file-columns"]["subcategory"]] in temp_sub_category:
                        temp_sub_category.append(row_regex[config["regex-file-columns"]["subcategory"]])
                        keyword_analysis_dictionary(row_regex[config["regex-file-columns"]["subcategory"]], "subcat")
                # Same as above for the cat
                if not row_regex[config["regex-file-columns"]["category"]] in temp_category :
                    temp_category.append(row_regex[config["regex-file-columns"]["category"]])
                    keyword_analysis_dictionary(row_regex[config["regex-file-columns"]["category"]], "cat")
        # Converting entries to string
        category.append(", ".join(temp_category))
        subcategory.append(", ".join(temp_sub_category))
        regex_output.append(", ".join(temp_regex))
    # Adding to df
    input_data["category"] = category
    input_data["subcategory"] = subcategory
    input_data["regex"] = regex_output

    if not config["INCLUDE_UNMATCH_RESULTS"]:
        input_data_2 = input_data[input_data["category"] != ""]
        input_data_2.to_csv(config["output-data"]["unmatched-data"], index=False)

    if config["TEST_OR_PROD"] == "Test":
        input_data.to_csv(config["output-data"]["test"], index=False)
        
    else:
        input_data.to_csv(config["output-data"]["prod"], index=False)

        
    print(category_keyword_count)
    print(subcat_keyword_count)
    sub_cat_analysis = pd.DataFrame(subcat_keyword_count.items(), columns=['Sub Category', 'Count'])
    cat_analysis = pd.DataFrame(category_keyword_count.items(), columns=['Category', 'Count'])

    sub_cat_analysis.to_csv(config["analysis_data"]["subcategory_file"], index=False)
    cat_analysis.to_csv(config["analysis_data"]["category_file"], index=False)

if __name__ == "__main__": 
    #Reading config file and loading in to variable
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    print("READING REGEX")
    regex_def = pd.read_csv(config["regex-file"])
    print("Data")
    if config["TEST_OR_PROD"] == "Test":
        data = pd.read_csv(config["input-data"]["test"], sep="\t")
    else:
        data = pd.read_csv(config["input-data"]["prod"])

    run_regex_search(data, regex_def)