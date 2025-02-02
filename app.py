from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Database and AI setup
connection_string = "mongodb+srv://senthilbhanavi:bf8GipzsPOALyoBg@cluster1.k0h8c.mongodb.net/"
client = MongoClient(connection_string)
db = client["Food"]
collection = db["recipes"]

# Configure Gemini AI
genai.configure(api_key="AIzaSyBvIuqa0GqJUrsIHDiYX3Rx90Onyl24JhQ")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("CatBotHomePage.html")

def find_recipe_by_title(title):
    # Query to find the recipe within the 'recipes' array
    recipe = collection.find_one({"Recipe Title": title}, {"_id": 0, "Recipe Title": 1, "Ingredients": 1})
    if recipe:
        return recipe["Recipe Title"], recipe["Ingredients"]
    else:
        return None

@app.route("/send-message", methods=["POST"])
def catch_user_input():
    data = request.get_json()
    title_input = data.get("message", "").strip()  # Fix missing title_input
    
    if not title_input:
        return jsonify({"error": "Title is required"}), 400

    print("starting search")
    recipe = find_recipe_by_title(title_input)
    print("recipe search")
    if recipe:
        print("found recipe")
        recipe_title, ingredients = recipe
        ingredients_text = ", ".join(ingredients)

        response = model.generate_content(
            f"Generate a recipe for {recipe_title} with these ingredients: {ingredients_text}. "
            "Format it like this: \nName: __ \nIngredients: __, __, __ \nSteps: \n1. __ \n2. __ \n3. __"
        )

        if hasattr(response, 'text'):
            return jsonify({"message": response.text})
        else:
            return jsonify({"error": "AI response format error"}), 500
    else:
        return jsonify({"error": "Recipe not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
