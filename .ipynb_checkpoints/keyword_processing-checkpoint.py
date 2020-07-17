def keyword_processing(df):
    """Input must be a pandas dataframe."""

    import kwgen
    import pandas as pd
    #df = pd.read_csv(input_file, sep=",")

    # Assign function selection to a variable
    choice =  df.iloc[0,1]

    if choice == 1: # Standalone keyword generation
        em = kwgen.standalone_kw_em(df)
        mbm = kwgen.standalone_kw_mbm(df)
  
        final = pd.concat([em, mbm])
        #final.to_csv("output.csv", sep=",", index=False)
        
        message = "Done"
  
    elif choice == 2: # Bigram keyword generation
        em = kwgen.igram_kw_em(df)
        mbm = kwgen.bigram_kw_mbm(df)
        
        final = pd.concat([em, mbm])
        #final.to_csv("output.csv", sep=",", index=False)
        
        message = "Done"
        
    elif choice == 3: # Trigram keyword generation
        em = kwgen.trigram_kw_em(df)
        mbm = kwgen.trigram_kw_mbm(df)
        
        final = pd.concat([em, mbm])
        #final.to_csv("output.csv", sep=",", index=False)
        
        message = "Done"
        
    else:
        message = "Invalid selection, please enter 1, 2, or 3 in 'Choice'."
        final = None

    print(choice)
    print(message)
    
    # return the dataframe to the app
    return final
