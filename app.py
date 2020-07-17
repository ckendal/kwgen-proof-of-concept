from flask import Flask, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
#import kwgen as kwgen
from os import environ
#from keyword_processing import keyword_processing
#from werkzeug import secure_filename

#UPLOAD_FOLDER = '/path/to/the/uploads'
#ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#-- Define functions
def standalone_kw_mbm(df):
    """This is a function to generate Modified Broad Match (MBM) standalone keywords for major product categories. Accepts a Pandas DataFrame as input, must have columns named 'Campaign', 'H1', and 'Final URL'."""
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
            
          #Create keyword identifier: this is to help assign ad group
          kw_id = desc + "|" + final_urls[k]
          
          #Append results to the appropriate list
      
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

#--


# Original code (for reference)
"""
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
"""
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        try: 
            # File Input: CSV link or upload, convert to string
            input_file = str(request.form['content'])
            df = pd.read_csv(input_file, sep=",")
            #dataset.to_csv("output.csv", sep=",", index=False)
            
            
            choice =  df.iloc[0,1]

            if choice == 1: # Standalone keyword generation
                em = standalone_kw_em(df)
                mbm = standalone_kw_mbm(df)
  
                final = pd.concat([em, mbm])
                #final.to_csv("output.csv", sep=",", index=False)
        
                message = "Done"
  
            elif choice == 2: # Bigram keyword generation
                em = bigram_kw_em(df)
                mbm = bigram_kw_mbm(df)
        
                final = pd.concat([em, mbm])
                #final.to_csv("output.csv", sep=",", index=False)
        
                message = "Done"
            
            elif choice == 3: # Trigram keyword generation
                em = trigram_kw_em(df)
                mbm = trigram_kw_mbm(df)
        
                final = pd.concat([em, mbm])
                #final.to_csv("output.csv", sep=",", index=False)
        
                message = "Done"
        
            else:
                message = "Invalid selection, please enter 1, 2, or 3 in 'Choice'."
                final = None

            print(choice)
            print(message)
            
            
            # process the keywords
            #process = bigram_kw_em(dataset)
            
            final.to_csv("output.csv", sep=",", index=False)
                
            
            # Display the first line of the csv on screen
            #return dataset.head(1).to_html()
            
            #return redirect('/')
            
            return send_file("output.csv", as_attachment=True)
            #return render_template("download.html")
        
        except:
            return 'There was an issue importing your file. Please make sure the file type is CSV and data is formatted properly.'
        
        #else:
            #return send_file("output.csv", as_attachment=True)
    else:
        #tasks = Todo.query.order_by(Todo.date_created).all()
        #return render_template("download.html",output="output.csv")
        #return redirect('/')
        #dataset = pd.read_csv(input_file, sep=",")
        
        return render_template('index.html')


@app.route('/download/', methods=["GET"])
def download():
    if request.method == "GET":
        return send_file("output.csv", as_attachment=True)
    else:
        return "Yeet"



"""
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)
"""

"""
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
"""

if __name__ == "__main__":
    app.run(debug=True)
