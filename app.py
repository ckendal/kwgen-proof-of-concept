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
            # File Input: CSV link or upload, convert to string
            input_file = str(request.form['content'])
            df = pd.read_csv(input_file, sep=",", dtype='str', encoding='utf-8')

            # Generate keywords from the input file
            output = process_keywords(df)

            # Convert the output DataFrame to a CSV
            output.to_csv("output.csv", sep=",", index=False)

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