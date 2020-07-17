# -*- coding: utf-8 -*-
"""kwgen_beta.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d6UY6gAtLabMGRAY3e1pckjCg1Wxxbui

# Kwgen: KeyWord GENerator
Omnitail, LLC.

(Beta Release)

As this is still a beta version of the product, please feel free to get in touch with me regarding any questions, concerns, or suggestions. This tool is for your convenience, your input means a lot!

Thanks,

Chris

# 1. Getting Started

## Input
When you start the program, you will be prompted to enter an input file name into a text box. There are 2 ways to do this.

Upload CSV via UI:
- Click 'Connect' in the top-right corner to connect to the server.
- Expand the left sidebar
- Select 'Files'
- Click 'Upload'
- Type the file name into the text box when prompted,
- OR, right-click the file in the side bar:
  - Select 'Copy Path'
  - Paste this result into the text box when prompted.

Import CSV from a Google Sheet:
- In Google Sheets, publish your desired sheet to the web as a CSV.
- Paste the published URL into the text box when prompted.

## Run
Once your have your input file ready:
- Select 'Runtime' from the top menu bar.
- Select 'Run All'
- Enter your input file name into the text box when prompted, then hit the 'Enter' key.
"""

input_file = str(input(prompt="Please Enter a filename: "))

input_file

"""# 2. Operation

### Functions

#### 1gram Functions
"""

def standalone_kw_mbm(df):
  """This is a function to generate Modified Broad Match (MBM) standalone keywords for major product categories.
  Accepts a Pandas DataFrame as input, must have columns named 'Campaign', 'H1', and
  'Final URL'."""
  
  import pandas as pd
  
  # Convert dataframe series to lists
  #campaign_name = df["Campaign"].tolist()
  campaign_name = df.iloc[0, 0]
  
  h1 = df["H1"].dropna().tolist()
  final_urls = df["Final URL"].dropna().tolist()
  status = "Paused"
  
  # Initialize lists to store dataset values
  campaign_col = []         # List: campaign names
  campaign_status = []      # List: campaign status
  match_type = []           # List: keyword match type
  ad_groups = []            # List: ad group names
  urls = []                 # List: final URLs
  kw = []                   # List: keywords
  
  # Iterate through the terms to generate keywords
  for i in range(len(h1)):
    
    mbm_kw = h1[i]
    mbm_kw = mbm_kw.replace(" ", " +")
    # Append " +" before kw string; Leading space necessary so Excel does not parse the keyword as a formula.
    mbm_kw = " +" + mbm_kw
    
    ad_group_name = campaign_name + " - " + h1[i] + " - MBM"
    
    # Append results to the appropriate list
    kw.append(mbm_kw)
    ad_groups.append(ad_group_name)
    urls.append(final_urls[i])
    campaign_col.append(campaign_name)
    match_type.append("Broad")
    campaign_status.append(status)
    
  # Dictionary for output
  keyword_dict = {"Campaign": campaign_col, "Campaign Status": campaign_status,
                  "Ad Group": ad_groups, "Keyword": kw, 
                  "Match Type": match_type, "Final Url": urls}
  
  # Store the dictionary's data to a DataFrame
  df = pd.DataFrame(data = keyword_dict)
  
  return df

def standalone_kw_em(df):
  """This is a function to generate Exact Match (EM) standalone keywords for major product categories.
  Accepts a Pandas DataFrame as input, must have columns named 'Campaign', 'H1', and
  'Final URL'."""
  
  import pandas as pd
  
  campaign_name = df.iloc[0, 0]

  # Convert dataframe series to lists
  #campaign_name = df["Campaign"].tolist()
  h1 = df["H1"].dropna().tolist()
  final_urls = df["Final URL"].dropna().tolist()
  status = "Paused"
  
  # Initialize lists to store dataset values
  campaign_col = []         # List: campaign names
  campaign_status = []      # List: campaign status
  match_type = []           # List: keyword match type
  ad_groups = []            # List: ad group names
  urls = []                 # List: final URLs
  kw = []                   # List: keywords
  
  # Iterate through the terms to generate keywords
  for i in range(len(h1)):
    
    em_kw = h1[i]
    ad_group_name = campaign_name + " - " + h1[i] + " - EM"
    
    # Append results to the appropriate list
    kw.append(em_kw)
    ad_groups.append(ad_group_name)
    urls.append(final_urls[i])
    campaign_col.append(campaign_name)
    match_type.append("Exact")
    campaign_status.append(status)
    
  # Dictionary for output
  keyword_dict = {"Campaign": campaign_col, "Campaign Status": campaign_status,
                  "Ad Group": ad_groups, "Keyword": kw, 
                  "Match Type": match_type, "Final Url": urls}
  
  # Store the dictionary's data to a DataFrame
  df = pd.DataFrame(data = keyword_dict)
  
  return df

"""#### 2gram Functions"""

## Changes in v 2.0
### Remove Final URL
### Add campaign status feature
### Pass campaign name in the input sheet instead of in the function itself

def bigram_kw_em(df):
  """This is a function to generate keywords out of permutations of 2 words or phrases.
 The output of this function is a dictionary. In this case h1 are descriptors
 and h2 terms are the nouns to be modified.
 Inputs: 'campaign_name' must be a string, 'h1' and 'h2' must be lists, but do not need to have the same length.
 List of final_urls must be same length as h2. Pandas is a dependency of this function.
 Campaign_name must be a string and df must be a Pandas dataframe."""
  
  import pandas as pd
  
  campaign_name = df.iloc[0, 0]
  h1 = df["H1"].dropna().tolist()
  h2 = df["H2"].dropna().tolist()
  status = "Paused"
  final_urls = df["Final URL"].dropna().tolist()
  
  ###
  # Parse optional input column for 'Theme' column to group similar H1 terms
  h1_themes = df["H1 Theme"].fillna(0).tolist()
  
  themes = []  # List to store H1 theme for output file
  ###
  
  campaign_col = [] # List to store campaign names
  match_type = [] # List to store keyword match type
  descriptors = [] # List to store descriptors, useful for manual ad group assignment
  campaign_status = []
  urls = []
  ids = [] # List to store keyword identifiers
  base = []  # List to store base terms being modified
  
  # List to store keyword permutations
  kw = []
  
  # Iterate through the h1 and h2 terms to generate keywords
  for i in range(len(h1)):
    
    for j in range(len(h2)):
      
      # Assign the descriptor to a variable
      desc = h1[i]
      
      exact_kw = str(h1[i]) + " " + str(h2[j])
      
      # Create keyword identifier: this is to help assign ad group
      kw_id = desc + "|" + final_urls[j]
    
      # Append results to the appropriate list
      descriptors.append(desc)
      kw.append(exact_kw) # keyword
      campaign_col.append(campaign_name)
      match_type.append("Exact")
      campaign_status.append(status)
      urls.append(final_urls[j])
      ids.append(kw_id)
      base.append(h2[j])
      
      ###
      themes.append(h1_themes[i])
    
  # Dictionary for output
  keyword_dict = {"Campaign": campaign_col, 
                  "Campaign Status": campaign_status,
                  "Keyword": kw , 
                  "Match Type": match_type,
                  "H1 Theme": themes, 
                  "Descriptor": descriptors, 
                  "Base Term": base, 
                  "Final Url": urls,
                  "Identifier": ids}
  
  # Store the dictionary's data to a DataFrame
  df = pd.DataFrame(data = keyword_dict)
  
  return df

## Changes in v 2.0
### Remove Final URL
### Add campaign status feature
### Pass campaign name in the input sheet instead of in the function itself

# replace 'em' with 'mbm', add text to change kw and match type

def bigram_kw_mbm(df):
  """This is a function to generate keywords out of permutations of 2 words or phrases.
 The output of this function is a dictionary. In this case h1 are descriptors
 and h2 terms are the nouns to be modified.
 Inputs: 'campaign_name' must be a string, 'h1' and 'h2' must be lists, but do not need to have the same length.
 List of final_urls must be same length as h2. Pandas is a dependency of this function.
 Campaign_name must be a string and df must be a Pandas dataframe."""
  
  import pandas as pd
  
  campaign_name = df.iloc[0, 0]
  h1 = df["H1"].dropna().tolist()
  h2 = df["H2"].dropna().tolist()
  status = "Paused"
  final_urls = df["Final URL"].dropna().tolist()
  
  ###
  # Parse optional input column for 'Theme' column to group similar H1 terms
  h1_themes = df["H1 Theme"].fillna(0).tolist()
  
  themes = []  # List to store H1 theme for output file
  ###
  
  campaign_col = [] # List to store campaign names
  match_type = [] # List to store keyword match type
  descriptors = [] # List to store descriptors, useful for manual ad group assignment
  campaign_status = []
  urls = []
  ids = [] # List to store keyword identifiers
  base = []  # List to store base terms being modified
  
  # List to store keyword permutations
  kw = []
 
  # Iterate through the h1 and h2 terms to generate keywords
  for i in range(len(h1)):
    
    for j in range(len(h2)):
      
      # Assign current descriptor to a variable
      desc = h1[i]
      
      mbm_kw = str(h1[i]) + " " + str(h2[j])
      
      # Append '+' wheverever a space is present in keyword
      mbm_kw = mbm_kw.replace(" ", " +")
      
      # Append " +" before kw string; Leading space necessary so Excel does not parse the keyword as a formula.
      mbm_kw = " +" + mbm_kw
      mbm_kw = str(mbm_kw)
      
      # Create keyword identifier: this is to help assign ad group
      kw_id = desc + "|" + final_urls[j]
      
      # Append results to the appropriate list
      kw.append(mbm_kw) # keyword
      descriptors.append(desc)
      campaign_col.append(campaign_name)
      match_type.append("Broad")
      campaign_status.append(status)
      urls.append(final_urls[j])
      ids.append(kw_id)
      base.append(h2[j])
      
      ###
      themes.append(h1_themes[i])
 
  # Dictionary for output
  keyword_dict = {"Campaign": campaign_col, 
                  "Campaign Status": campaign_status,
                  "Keyword": kw , 
                  "Match Type": match_type,
                  "H1 Theme": themes, 
                  "Descriptor": descriptors, 
                  "Base Term": base, 
                  "Final Url": urls,
                  "Identifier": ids}
  
  # Store the dictionary's data to a DataFrame
  df = pd.DataFrame(data = keyword_dict)
  
  return df

"""#### 3gram Functions"""

def trigram_kw_em(df):
  """This is a function to generate keywords out of permutations of 2 words or phrases.
 The output of this function is a dictionary. In this case h1 are descriptors
 and h2 terms are the nouns to be modified.
 Inputs: 'campaign_name' must be a string, 'h1' and 'h2' must be lists, but do not need to have the same length.
 List of final_urls must be same length as h2. Pandas is a dependency of this function.
 Campaign_name must be a string and df must be a Pandas dataframe."""
  
  import pandas as pd
  
  campaign_name = df.iloc[0, 0]
  h1 = df["H1"].dropna().tolist()
  h2 = df["H2"].dropna().tolist()
  h3 = df["H3"].dropna().tolist()
  status = "Paused"
  final_urls = df["Final URL"].dropna().tolist()
  
  campaign_col = [] # List to store campaign names
  match_type = [] # List to store keyword match type
  descriptors = [] # List to store descriptors, useful for manual ad group assignment
  campaign_status = []
  urls = []
  ids = [] # List to store keyword identifiers
  base = []  # List to store base terms being modified
  
  # List to store keyword permutations
  kw = []
  
  # Iterate through the h1 and h2 terms to generate keywords
  for i in range(len(h1)):
    
    for j in range(len(h2)):
      
      for k in range(len(h3)):
        # Assign the descriptor to a variable
        desc = h1[i] + "|" + h2[j]
        
        exact_kw = str(h1[i]) + " " + str(h2[j]) + " " + str(h3[k])
        
        # Create keyword identifier: this is to help assign ad group
        kw_id = desc + "|" + final_urls[k]
        
        # Append results to the appropriate list
        descriptors.append(desc)
        kw.append(exact_kw) # keyword
        campaign_col.append(campaign_name)
        match_type.append("Exact")
        campaign_status.append(status)
        urls.append(final_urls[k])
        ids.append(kw_id)
        base.append(h3[k])
    
  # Dictionary for output
  keyword_dict = {"Campaign": campaign_col, 
                  "Campaign Status": campaign_status,
                  "Keyword": kw , 
                  "Match Type": match_type,
                  "Descriptor": descriptors, 
                  "Base Term": base,
                  "Final Url": urls,
                  "Identifier": ids}
  
  # Store the dictionary's data to a DataFrame
  df = pd.DataFrame(data = keyword_dict)
  
  return df

def trigram_kw_mbm(df):
  """This is a function to generate keywords out of permutations of 2 words or phrases.
 The output of this function is a dictionary. In this case h1 are descriptors
 and h2 terms are the nouns to be modified.
 Inputs: 'campaign_name' must be a string, 'h1' and 'h2' must be lists, but do not need to have the same length.
 List of final_urls must be same length as h2. Pandas is a dependency of this function.
 Campaign_name must be a string and df must be a Pandas dataframe."""
  
  import pandas as pd
  
  campaign_name = df.iloc[0, 0]
  h1 = df["H1"].dropna().tolist()
  h2 = df["H2"].dropna().tolist()
  h3 = df["H3"].dropna().tolist()
  status = "Paused"
  final_urls = df["Final URL"].dropna().tolist()
  
  campaign_col = [] # List to store campaign names
  match_type = [] # List to store keyword match type
  descriptors = [] # List to store descriptors, useful for manual ad group assignment
  campaign_status = []
  urls = []
  ids = [] # List to store keyword identifiers
  base = []  # List to store base terms being modified
  
  # List to store keyword permutations
  kw = []
  
  # Iterate through the h1 and h2 terms to generate keywords
  for i in range(len(h1)):
    
    for j in range(len(h2)):
      
      for k in range(len(h3)):
        # Assign the descriptor to a variable
        desc = h1[i] + "|" + h2[j]
        
        mbm_kw = str(h1[i]) + " " + str(h2[j]) + " " + str(h3[k])
        
        # Append '+' to keywords
        mbm_kw = mbm_kw.replace(" ", " +")
        
        # Append " +" before kw string; Leading space necessary so Excel does not parse the keyword as a formula.
        mbm_kw = " +" + mbm_kw
        
        # Create keyword identifier: this is to help assign ad group
        kw_id = desc + "|" + final_urls[k]
        
        # Append results to the appropriate list
        descriptors.append(desc)
        kw.append(mbm_kw) # keyword
        campaign_col.append(campaign_name)
        match_type.append("Broad")
        campaign_status.append(status)
        urls.append(final_urls[k])
        ids.append(kw_id)
        base.append(h3[k])
    
  # Dictionary for output
  keyword_dict = {"Campaign": campaign_col, 
                  "Campaign Status": campaign_status,
                  "Keyword": kw , 
                  "Match Type": match_type,
                  "Descriptor": descriptors, 
                  "Base Term": base,
                  "Final Url": urls,
                  "Identifier": ids}
  
  # Store the dictionary's data to a DataFrame
  df = pd.DataFrame(data = keyword_dict)
  
  return df

"""### Processing"""

import pandas as pd
dataset = pd.read_csv(input_file, sep=",")

# Assign function selection to a variable
choice =  dataset.iloc[0,1]

if choice == 1: # Standalone keyword generation
  em = standalone_kw_em(dataset)
  mbm = standalone_kw_mbm(dataset)
  
  final = pd.concat([em, mbm])
  final.to_csv("output.csv", sep=",", index=False)
  
  message = "Done"
  
elif choice == 2: # Bigram keyword generation
  em = bigram_kw_em(dataset)
  mbm = bigram_kw_mbm(dataset)
  
  final = pd.concat([em, mbm])
  final.to_csv("output.csv", sep=",", index=False)
  
  message = "Done"

elif choice == 3: # Trigram keyword generation
  
  em = trigram_kw_em(dataset)
  mbm = trigram_kw_mbm(dataset)
  
  final = pd.concat([em, mbm])
  final.to_csv("output.csv", sep=",", index=False)
  
  message = "Done"
  
else:
  
  message = "Invalid selection, please enter 1, 2, or 3 in 'Choice'."

"""# 3. Completion Status

Once the program has finished running, you will recieve 2 lines of output text.

The first line will have a number corresponding to the type of keywords that were generated:
- 1: One-gram keywords.
- 2: Bigram keywords.
- 3: Trigram keywords.

The second line will be the completion status.
- If the program ran successfully, the output will be 'Done'
- If a value other than 1, 2, or 3 was in the 'Choice' column in the input sheet, you will recieve an error message.
"""

print(choice)
print(message)

"""# 4. Retrieving The Output File
- Expand the left sidebar
- Select 'Files'
- Right-click 'output.csv' to download the file.

Note: If you double-click on 'output.csv', you can see a preview of the output file.

# 5. Troubleshooting
Coming soon.
"""