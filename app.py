from flask import Flask, jsonify
import pandas as pd
import app_model

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    
    return jsonify({"message": "This is book recommendation system. Please call /recommend-books function to get recommendations."})

@app.route("/refresh-data", methods=["GET"])
def refresh_data_endpoint():
    app_model.Crawler.RefreshData()
    return jsonify({"message": app_model.Crawler.RefreshData()})


@app.route("/recommend-books", methods=["POST"])
def recommend_books_endpoint():
    

    try:
        # favorite_book = str(favorite_book = request.json["favorite-book"])
        favorite_book = "1984"

        dataStorage = app_model.DataStorage()
        recomEngine = app_model.RecommendationEngine(dataStorage)
        recommended_books = recomEngine.RecommendBooks(favorite_book)
        
        return recommended_books.to_json(orient='records')
        #return jsonify({ recommended_books.to_json(orient='records') })
    except () as e:
        return {"message": str(e)}, 400

    

