import google.generativeai as genai
from pymongo import MongoClient

connection_string = "mongodb+srv://senthilbhanavi:bf8GipzsPOALyoBg@cluster1.k0h8c.mongodb.net/"

client = MongoClient(connection_string)

genai.configure(api_key="AIzaSyBvIuqa0GqJUrsIHDiYX3Rx90Onyl24JhQ")
model = genai.GenerativeModel("gemini-1.5-flash")

db = client["Food"]
collection = db["recipes"]

def find_recipe_by_title(title):
    # Query to find the recipe within the 'recipes' array
    recipe = collection.find_one({"Recipe Title": title}, {"_id": 0, "Recipe Title": 1, "Ingredients": 1})
    if recipe:
        return recipe["Recipe Title"], recipe["Ingredients"]
    else:
        return None




if __name__ == "__main__":
    # Example usage
    title_input = "Caesar Salad" #string
    result = find_recipe_by_title(title_input)
    if result:
        recipe_title, ingredients = result
        ingredientsFinal = ", ".join(ingredients)
        response = model.generate_content(
            f"generate a recipe for making {recipe_title} given these ingredients: {ingredientsFinal}. "
            "And do it in this format: \nName: __ \nIngredients: __, __, __ \nStep 1: __ \nStep 2: __ \nStep 3: __ \n..."
        )
        print(response.text)
    else:
        print("Recipe not found")

    
