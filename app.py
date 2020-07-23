from flask import Flask, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from itertools import product

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        try: 
            # File Input: CSV link or upload, convert to string
            input_file = str(request.form['content'])
            df = pd.read_csv(input_file, sep=",", dtype='str', encoding='utf-8')

            # Extract the campaign name
            campaign_name = str(df.loc[0, "Campaign Name"])

            # remove the campaign name column from the dataframe
            df = df.drop(columns=["Campaign Name"])
            
            # count number of remaining columns in the dataframe
            col_num = len(df.columns)

            # Create a dictionary to store lists of each column of the dataframe. Each key is the column name
            col_names = list(df.columns)
            cd = dict()

            # iterate through columns, assign list of values to a corresponding dictionary key
            # convert columns to lists
            for element in col_names:
                cd[element] = df[element].dropna().tolist()

            # need to add support for a single input column

            if col_num == 2:
                final = list(product(cd[col_names[0]], cd[col_names[1]]))
            elif col_num == 3:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]]))
            elif col_num == 4:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]], cd[col_names[3]]))
            elif col_num == 5:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]], cd[col_names[3]], cd[col_names[4]]))
            elif col_num == 6:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]], cd[col_names[3]], cd[col_names[4]], cd[col_names[5]]))
            elif col_num == 7:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]], cd[col_names[3]], cd[col_names[4]], cd[col_names[5]], cd[col_names[6]]))
            elif col_num == 8:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]], cd[col_names[3]], cd[col_names[4]], cd[col_names[5]], cd[col_names[6]], cd[col_names[7]]))
            elif col_num == 9:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]], cd[col_names[3]], cd[col_names[4]], cd[col_names[5]], cd[col_names[6]], cd[col_names[7]], cd[col_names[8]]))
            elif col_num == 10:
                final = list(product(cd[col_names[0]], cd[col_names[1]], cd[col_names[2]], cd[col_names[3]], cd[col_names[4]], cd[col_names[5]], cd[col_names[6]], cd[col_names[7]], cd[col_names[8]], cd[col_names[9]]))
            else:
                # put an error statement here
                pass

            final = pd.DataFrame(final)

            # Concatenate keywords
            em_kw = [] # list for exact match keywords
            mbm_kw = [] # list for modified broad match keywords
            for i in range(len(final)):
                word =  " ".join(list(final.iloc[i]))
                em = "[" + word + "]"
                mbm = word.replace(" "," +")
                mbm = " +" + mbm
                
                em_kw.append(em)
                mbm_kw.append(mbm)

            # Create lists of keyword match types
            match_em = ["Exact"] * len(em_kw)
            match_mbm = ["Broad"] * len(mbm_kw)

            em_kw = pd.DataFrame(em_kw, columns=["Keyword"])
            mbm_kw = pd.DataFrame(mbm_kw, columns=["Keyword"])

            # Append keyword match types to dataframes
            em_kw["Match Type"] = match_em
            mbm_kw["Match Type"] = match_mbm

            keyword_output = pd.concat([em_kw, mbm_kw])

            # Insert campaign name into the output file
            campaign_name_col = [campaign_name] * len(keyword_output)
            keyword_output.insert(0, "Campaign Name", campaign_name_col)

            # Convert the output DataFrame to a CSV
            keyword_output.to_csv("output.csv", sep=",", index=False)
            
            # Return the output file to trigger the download
            return send_file("output.csv", as_attachment=True)
        
        except:
            # Error message if CSV failed to import or was not formatted properly
            return 'There was an issue importing your file. Please make sure the file type is CSV and data is formatted properly.'
        
    else:
        # If a POST request is not made then display the homepage until input is registered.
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)