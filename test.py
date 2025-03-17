from flask import Flask, jsonify
import pandas as pd
import app_model
import os
#import kagglehub

#os.environ["KAGGLE_CONFIG_DIR"] = "/path/to/your/kaggle.json"

#def main():
#    # Sample DataFrame
#    df = pd.DataFrame({
#        'A': [1, 2, 3],
#        'B': [4, 5, 6]
#    })
#    
#    print(df)
#    # Convert DataFrame to JSON
#    json_data = df.to_json(orient='records')
#    print(json_data)

def RecommendTest():
    engine = app_model.RecommendationEngine(dataStorage=app_model.DataStorage())
    favoriteBook = '1984'

    recommended_books = engine.RecommendBooks(favoriteBook)
    print(recommended_books)
    
    s1 = recommended_books.to_json(orient='records')

def main():
    RecommendTest()

# This block ensures the script runs only when executed directly (not imported as a module)
if __name__ == "__main__":
    main()  # Call the main function



    #jsonRecommended_books = jsonify({ recommended_books })

    #print( jsonRecommended_books)

# def main():
#     destination_path = "data/"
#     print("Hello world: " + destination_path)
#     
#     os.chdir(destination_path)
# 
#     # Download latest version from Kaggle Hub    
#     path = kagglehub.dataset_download("jirakst/bookcrossing")
#     str(path)







#def TestKaggle():
#    destination_path = "/app/data/"
#        
#    os.chdir(destination_path)
#    # Download latest version from Kaggle Hub
#    
#    #path = kagglehub.dataset_download("jirakst/bookcrossing")
#    #str(os.listdir(path))
#    print(str(kagglehub.config()))


