# tagging_engine.py

from typing import List, Dict

def tag_category(name: str, macros: Dict) -> List[str]:
    name = name.lower()
    tags = []
    if any(x in name for x in ["chicken", "beef", "pork", "lamb", "fish", "egg", "turkey", "salmon", "yogurt", "cheese"]):
        tags.append("animal_proteins")
    if any(x in name for x in ["tofu", "tempeh", "lentil", "bean", "chickpea", "falafel"]):
        tags.append("plant_proteins")
    if any(x in name for x in ["rice", "potato", "bread", "pasta", "quinoa", "oats", "grain"]):
        tags.append("starchy_carbs")
    if any(x in name for x in ["spinach", "kale", "zucchini", "tomato", "onion", "carrot", "pepper", "broccoli"]):
        tags.append("non_starchy_veg")
    if any(x in name for x in ["oil", "avocado", "almond", "peanut", "seed", "butter", "nuts", "sunflower"]):
        tags.append("healthy_fats")
    if any(x in name for x in ["garlic", "lemon", "vinegar", "chili", "spice", "ginger", "mustard"]):
        tags.append("flavor_bases")
    if any(x in name for x in ["sauce", "dressing", "salsa", "gravy", "yogurt"]):
        tags.append("sauces")
    if any(x in name for x in ["herb", "parsley", "cilantro", "flake", "crunch", "pickle"]):
        tags.append("toppings")
    return list(set(tags))

def tag_dietary(name: str) -> List[str]:
    name = name.lower()
    tags = []
    if any(x in name for x in ["chicken", "beef", "fish", "egg", "yogurt", "cheese", "ham", "pork", "turkey"]):
        tags.append("non_vegan")
    if any(x in name for x in ["milk", "cheese", "yogurt", "whey", "cream"]):
        tags.append("dairy")
    if any(x in name for x in ["bread", "pasta", "wheat", "flour", "cracker"]):
        tags.append("gluten")
    if any(x in name for x in ["almond", "walnut", "cashew", "peanut", "hazelnut"]):
        tags.append("nut")
    if "soy" in name or "tofu" in name or "tempeh" in name:
        tags.append("soy")
    if any(x in name for x in ["bean", "lentil", "chickpea", "pea"]):
        tags.append("legume")
    return tags

def tag_nutrition(macros: Dict, micros: Dict) -> List[str]:
    tags = []
    protein = macros.get("protein_g", 0)
    fat = macros.get("fat_g", 0)
    carbs = macros.get("carbs_g", 0)
    kcal = macros.get("calories_kcal", 1)  # prevent divide by zero

    if protein >= 8:
        tags.append("high_protein")
    if fat <= 3:
        tags.append("low_fat")
    if fat >= 15:
        tags.append("high_fat")
    if carbs <= 5:
        tags.append("low_carb")
    if macros.get("fiber_g", 0) >= 4:
        tags.append("high_fiber")
    if micros.get("calcium_mg", 0) >= 100:
        tags.append("high_calcium")
    if micros.get("magnesium_mg", 0) >= 40:
        tags.append("high_magnesium")
    if micros.get("choline_mg", 0) >= 50:
        tags.append("high_choline")
    if micros.get("iron_mg", 0) >= 2:
        tags.append("high_iron")

    # Protein per kcal
    ratio = round(protein / kcal, 3)
    if protein >= 8 and ratio >= 0.2:
        tags.append("lean_protein_source")

    return tags, ratio

def tag_cuisine(name: str) -> List[str]:
    name = name.lower()
    tags = []
    if any(x in name for x in ["paneer", "dal", "masoor", "ghee"]):
        tags.append("indian")
    if any(x in name for x in ["chorizo", "tortilla", "tamale"]):
        tags.append("latin")
    if any(x in name for x in ["soy", "tofu", "miso", "bok choy"]):
        tags.append("asian")
    if any(x in name for x in ["olive", "feta", "yogurt", "parsley"]):
        tags.append("mediterranean")
    if any(x in name for x in ["tahini", "bulgur", "lamb"]):
        tags.append("middle_eastern")
    if any(x in name for x in ["cheddar", "turkey", "white bread"]):
        tags.append("american")
    if any(x in name for x in ["sausage", "rye", "butter", "cabbage"]):
        tags.append("european")
    return tags
