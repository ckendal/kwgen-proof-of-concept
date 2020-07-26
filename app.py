from flask import Flask, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from itertools import product
from kwgen import process_keywords

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        try:
            # File imports: link to CSV or XLSX (Excel spreadsheet), convert to string
            input_file = str(request.form['content'])

            # Check if the input file is a CSV or XLSX file
            if input_file.endswith("csv"):
                # Import the CSV file as a pandas DataFrame
                df = pd.read_csv(input_file, sep=",", dtype='str', encoding='utf-8')

                # Generate keywords from the input sheet
                output = process_keywords(df)

                # Convert the output DataFrame to a CSV
                output.to_csv("output.csv", sep=",", index=False)

                # Return the output file to trigger the download
                return send_file("output.csv", as_attachment=True)


            elif input_file.endswith("xlsx"):
            #else:
                # Import the xlsx file as a dict of DataFrames
                spreadsheet = pd.read_excel(input_file, sheet_name=None)
                
                # Create a list of sheet names from the spreadsheet dict keys
                sheet_names = list(spreadsheet.keys())


                # Keyword Processing: Iterate through the dict keys for each sheet's DataFrame
                for key in sheet_names:
                    # Process the keywords in each DataFrame and update that dataframe into keyword output
                    spreadsheet[key] = process_keywords(spreadsheet[key])

                
                #-- Create output file: Concatenate all the output sheets into a single file --#
                # Create a list of all the spreadsheet elements
                output_list = []

                # Iterate through all the sheets in the spreadsheet
                for sheet in spreadsheet:
                    # Assign the dataframe to a variable
                    key = spreadsheet[sheet]
                    # Append to the list
                    output_list.append(key)

                # Concatenate the list of dataframes into a single dataframe
                output = pd.concat(output_list)

                # Convert the output file to a CSV
                output.to_csv("output.csv", sep=",", index=False)

                # Return the output file as a download
                return send_file("output.csv", as_attachment=True)
                
        except:
            # Error message if CSV failed to import or was not formatted properly
            return 'There was an issue importing your file. Please make sure the file type is CSV or XLSX for and data is formatted properly.'
        
    else:
        # If a POST request is not made then display the homepage until input is registered.
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)