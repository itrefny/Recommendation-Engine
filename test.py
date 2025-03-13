from flask import Flask, jsonify
import pandas as pd
import app_model

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


def main():
    engine = app_model.RecommendationEngine(dataStorage=app_model.DataStorage())
    favoriteBook = '1984'

    recommended_books = engine.RecommendBooks(favoriteBook)
    print(type(recommended_books))
    
    s1 = recommended_books.to_json(orient='records')

    #jsonRecommended_books = jsonify({ recommended_books })

    #print( jsonRecommended_books)

# This block ensures the script runs only when executed directly (not imported as a module)
if __name__ == "__main__":
    main()  # Call the main function