# Function to generate keywords
"""
Inputs:
- dataframe
Dependencies
- from itertools import product
- import pandas as pd
Output:
- DataFrame
Notes:
- This should be in a function so the task can be repeated
if multiple sheets are input via an excel spreadsheet
"""

def process_keywords(dataset):
    """Add docstrings here"""
    import pandas as pd
    from itertools import product

    # Extract campaign name from first entry in 'Campaign Name' column
    campaign_name = str(dataset.loc[0,"Campaign Name"])

    # Remove the campaign name column from the dataframe
    dataset = dataset.drop(columns=["Campaign Name"])

    # Count number of remaining columns in the dataframe
    col_num = len(dataset.columns)

    # Create a dictionary to store lists of each column of the dataframe
    col_names = list(dataset.columns)
    col_dict = dict()

    # Iterate through columns, assign list of values to a corresponding key
    # Convert columns to lists
    for element in col_names:
        col_dict[element] = dataset[element].dropna().tolist()

    # Need to add support for a single input column (optional)
    if col_num == 2:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]]))
    elif col_num == 3:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]]))
    elif col_num == 4:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]], col_dict[col_names[3]]))
    elif col_num == 5:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]], col_dict[col_names[3]], col_dict[col_names[4]]))
    elif col_num == 6:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]], col_dict[col_names[3]], col_dict[col_names[4]], col_dict[col_names[5]]))
    elif col_num == 7:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]], col_dict[col_names[3]], col_dict[col_names[4]], col_dict[col_names[5]], col_dict[col_names[6]]))
    elif col_num == 8:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]], col_dict[col_names[3]], col_dict[col_names[4]], col_dict[col_names[5]], col_dict[col_names[6]], col_dict[col_names[7]]))
    elif col_num == 9:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]], col_dict[col_names[3]], col_dict[col_names[4]], col_dict[col_names[5]], col_dict[col_names[6]], col_dict[col_names[7]], col_dict[col_names[8]]))
    elif col_num == 10:
        final = list(product(col_dict[col_names[0]], col_dict[col_names[1]], col_dict[col_names[2]], col_dict[col_names[3]], col_dict[col_names[4]], col_dict[col_names[5]], col_dict[col_names[6]], col_dict[col_names[7]], col_dict[col_names[8]], col_dict[col_names[9]]))
    else:
        # put an error statement here
        pass

    # Convert the dictionary into a DataFrame
    final = pd.DataFrame(final)

    # Lists to store concatenated keywords by match type
    em_kw = [] # list for exact match keywords
    mbm_kw = [] # list for modified broad match keywords
    
    # Concatenate the terms in each permutation row into a keyword
    
    for i in range(len(final)): # Iterate each row of the DataFrame
        wordlist = list(final.iloc[i]) # Select row 'i' of the DataFrame       
        word = " ".join(wordlist) # Concatenate each term in the row with a space between each
        
        # Assign keyword match types
        em = "[" + word + "]"   # Use brackets to indicate Exact Match keywords
        mbm = word.replace(" "," +")    # Use + to indidcate Modified Broad Match keywords
        mbm = " +" + mbm
        
        # Append keywords to lists corresponding to their match type
        em_kw.append(em)
        mbm_kw.append(mbm)

    # Create lists of keyword match type indicators
    match_em = ["Exact"] * len(em_kw)
    match_mbm = ["Broad"] * len(mbm_kw)

    # Create DataFrames from each list of keywords
    em_kw = pd.DataFrame(em_kw, columns=["Keyword"])
    mbm_kw = pd.DataFrame(mbm_kw, columns=["Keyword"])

    # Append keyword match types to dataframes
    em_kw["Match Type"] = match_em
    mbm_kw["Match Type"] = match_mbm

    keyword_output = pd.concat([em_kw, mbm_kw])

    # Insert campaign name into the output file
    campaign_name_col = [campaign_name] * len(keyword_output)
    keyword_output.insert(0, "Campaign Name", campaign_name_col)

    # Return the output dataframe
    return keyword_output

#-- Function to split input file into smaller dataframes --#
def process_dataset(dataset):
    """Input a pandas dataframe and split it into separate dataframes of equal size. Then it will process the keywords.
    Returns a single dataframe of processed keywords"""
    import pandas as pd

    # Check number of columns in the dataframe
    col_count = len(list(dataset.columns))

    # List to return output dataframes (if necessary)
    df_output = []

    if col_count <= 11:
        #pass # do nothing if there are less than 11 columns in the input file (assumes the input is formatted properly)
        dataset = dataset.rename(columns={dataset.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        dataset = process_keywords(dataset)
        return dataset

    elif (col_count > 11) & (col_count <= 22): # Between 12 and 22 columns (corresponding to 2 input sheets)
        df1 = dataset.iloc[:,0:11].copy() # copy the original dataframe
        df1 = df1.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df1 = df1.rename(columns={df1.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df1 = process_keywords(df1) # Generate a dataframe of keywords from this dataframe
        df_output.append(df1) # append the dataframe to the list

        df2 = dataset.iloc[:,11:].copy() # copy the original dataframe
        df2 = df2.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df2 = df2.rename(columns={df2.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df2 = process_keywords(df2) # Generate a dataframe of keywords from this dataframe
        df_output.append(df2)

        # Concatenate output dataframes and return
        output_df = pd.concat([df_output[0], df_output[1]])
        return output_df
    
    elif (col_count > 22) & (col_count <= 33): # Between 23 and 33 columns
        df1 = dataset.iloc[:,0:11].copy() # copy the original dataframe
        df1 = df1.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df1 = df1.rename(columns={df1.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df1 = process_keywords(df1) # Generate a dataframe of keywords from this dataframe
        df_output.append(df1) # append the dataframe to the list

        df2 = dataset.iloc[:,11:22].copy() # copy the original dataframe
        df2 = df2.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df2 = df2.rename(columns={df2.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df2 = process_keywords(df2) # Generate a dataframe of keywords from this dataframe
        df_output.append(df2)

        df3 = dataset.iloc[:,22:].copy() # copy the original dataframe
        df3 = df3.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df3 = df3.rename(columns={df3.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df3 = process_keywords(df3) # Generate a dataframe of keywords from this dataframe
        df_output.append(df3)

        # Concatenate output dataframes and return
        output_df = pd.concat([df_output[0], df_output[1], df_output[2]])
        return output_df

    elif (col_count > 33) & (col_count <= 44): # Between 33 and 44 columns
        df1 = dataset.iloc[:,0:11].copy() # copy the original dataframe
        df1 = df1.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df1 = df1.rename(columns={df1.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df1 = process_keywords(df1) # Generate a dataframe of keywords from this dataframe
        df_output.append(df1) # append the dataframe to the list

        df2 = dataset.iloc[:,11:22].copy() # copy the original dataframe
        df2 = df2.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df2 = df2.rename(columns={df2.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df2 = process_keywords(df2) # Generate a dataframe of keywords from this dataframe
        df_output.append(df2)

        df3 = dataset.iloc[:,22:33].copy() # copy the original dataframe
        df3 = df3.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df3 = df3.rename(columns={df3.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df3 = process_keywords(df3) # Generate a dataframe of keywords from this dataframe
        df_output.append(df3)

        df4 = dataset.iloc[:,33:].copy() # copy the original dataframe
        df4 = df4.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df4 = df4.rename(columns={df4.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df4 = process_keywords(df4) # Generate a dataframe of keywords from this dataframe
        df_output.append(df4)

        # Concatenate output dataframes and return
        output_df = pd.concat([df_output[0], df_output[1], df_output[2], df_output[3]])
        return output_df

    elif (col_count > 44) & (col_count <= 55): # Between 44 and 55 columns
        df1 = dataset.iloc[:,0:11].copy() # copy the original dataframe
        df1 = df1.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df1 = df1.rename(columns={df1.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df1 = process_keywords(df1) # Generate a dataframe of keywords from this dataframe
        df_output.append(df1) # append the dataframe to the list

        df2 = dataset.iloc[:,11:22].copy() # copy the original dataframe
        df2 = df2.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df2 = df2.rename(columns={df2.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df2 = process_keywords(df2) # Generate a dataframe of keywords from this dataframe
        df_output.append(df2)

        df3 = dataset.iloc[:,22:33].copy() # copy the original dataframe
        df3 = df3.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df3 = df3.rename(columns={df3.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df3 = process_keywords(df3) # Generate a dataframe of keywords from this dataframe
        df_output.append(df3)

        df4 = dataset.iloc[:,33:44].copy() # copy the original dataframe
        df4 = df4.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df4 = df4.rename(columns={df4.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df4 = process_keywords(df4) # Generate a dataframe of keywords from this dataframe
        df_output.append(df4)

        df5 = dataset.iloc[:,44:].copy() # copy the original dataframe
        df5 = df5.dropna(how='all',axis='columns') # drop any columns that are completely empty
        df5 = df5.rename(columns={df5.columns[0]:"Campaign Name"}) # Rename the first column to 'Campaign Name'
        df5 = process_keywords(df5) # Generate a dataframe of keywords from this dataframe
        df_output.append(df5)

        # Concatenate output dataframes and return
        output_df = pd.concat([df_output[0], df_output[1], df_output[2], df_output[3], df_output[4]])
        return output_df

    