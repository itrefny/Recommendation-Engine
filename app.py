from flask import Flask, request, jsonify
import pandas as pd
import app_model
import json

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
        # Get JSON payload
        byteData = request.data
        json_str = byteData.decode('utf-8')        
        data = json.loads(json_str)

        favorite_book = data["favorite-book"]

        # Run recommendation engine
        dataStorage = app_model.DataStorage()
        recomEngine = app_model.RecommendationEngine(dataStorage)
        recommended_books = recomEngine.RecommendBooks(favorite_book)
        
        return jsonify( recommended_books.to_json(orient='records') )
    except () as e:
        return {"message": str(e)}, 400

    

