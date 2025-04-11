from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Flask Backend is Running!"})

@app.route('/get-commodities')
def get_commodities():
    return jsonify({"commodities": ["Select","Tomato",
    "Potato",
    "Onion",
    "Carrot",
    "Cabbage",
    "Carrot (Local)",
    "Brinjal",
    "Cabbage (Local)",
    "Radish Red",
    "Brinjal Long",
    "Soybean Green",
    "Garlic",
    "Ginger",
    "Peas",
    "Green Peas",
    "Smooth Gourd",
    "Sponge Gourd",
    "Radish White (Local)",
    "Chili",
    "Okra",
    "Squash (Long)",
    "Fenugreek",
    "Green Beans",
    "Jackfruit",
    "Broccoli",
    "Pointed Gourd (Local)",
    "Spinach Leaf",
    "Bamboo Shoot",
    "Sweet Potato",
    "Fenugreek Leaf",
    "Cauliflower (Local)",
    "Mustard Leaf",
    "Brinjal Round",
    "Broad Leaf Mustard",
    "Mushroom (Kanya)",
    "Christophine",
    "Asparagus",
    "Turnip A",
    "Brussels Sprout",
    "Chilli Green (Machhe)",
    "Mustard Greens",
    "Garlic Dry Chinese",
    "Mango (Maldah)",
    "Garlic Dry Nepali",
    "Sugarcane",
    "Chilli Green (Bullet)",
    "Rhubarb",
    "French Bean (Hybrid)",
    "Cauliflower",
    "Spinach",
    "Pumpkin",
    "Capsicum",
    "Radish",
    "Beetroot",
    "Ladyfinger",
    "Cucumber",
    "Mushroom",
    "Bitter Gourd",
    "Bottle Gourd",
    "Ash Gourd",
    "Drumstick",
    "Fenugreek Leaves",
    "Coriander",
    "Mint",
    "Spring Onion",
    "Turnip",
    "Sweet Corn",
    "Zucchini",
    "Celery",
    "Parsley",
    "Curry Leaves",
    "Red Cabbage",
    "Lettuce",
    "Kohlrabi",
    "Snake Gourd",
    "Ivy Gourd",
    "Cluster Beans",
    "French Beans",
    "Broad Beans",
    "Soybean",
    "Mustard Leaves",
    "Tapioca",
    "Jackfruit Seed",
    "Yam",
    "Colocasia",
    "Elephant Foot Yam"]})

@app.route('/get-prediction/<commodity>/<state>')
def get_prediction(commodity, state):
    # Load predictions file if it exists
    if os.path.exists("predictions.json"):
        with open("predictions.json", "r") as f:
            data = json.load(f)
        
        # Convert to lowercase for matching
        key = f"{commodity.lower()}_{state.lower()}"
        
        # Check if prediction exists
        if key in data:
            return jsonify(data[key])
    
    return jsonify({"error": "Prediction not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)


