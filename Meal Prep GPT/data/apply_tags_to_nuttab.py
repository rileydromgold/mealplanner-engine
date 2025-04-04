import json

# === Load raw NUTTAB data ===
with open("foundation_ingredients_nuttab.json", "r") as f:
    data = json.load(f)

# === Fields to retain ===
KEEP_FIELDS = {
    "name", "kcal", "protein_g", "fat_g", "carbs_g", "fiber_g",
    "calcium_mg", "iron_mg", "magnesium_mg", "zinc_mg", "copper_mg", "manganese_mg", "selenium_ug",
    "vitamin_a_rae_ug", "vitamin_c_mg", "vitamin_d_IU", "vitamin_e_mg", "vitamin_k_ug",
    "thiamin_mg", "riboflavin_mg", "niacin_mg", "vitamin_b6_mg", "folate_total_ug",
    "vitamin_b12_ug", "pantothenic_acid_mg", "choline_mg",
    "tags", "usage_weight_class"
}

# === Safe float parser (with passed-in ingredient)
def val(field, ing):
    try:
        raw = str(ing.get(field, "")).replace(",", "").strip()
        return float(raw) if raw else None
    except:
        return None

# === Weight class inference
def infer_usage_weight_class(name: str) -> str:
    name = name.lower()
    micro_keywords = ["chili", "cinnamon", "ginger", "nutmeg", "spice", "herb", "vanilla", "pepper", "clove", "zest", "saffron"]
    modest_keywords = ["oil", "sauce", "seed", "dressing", "flax", "chia", "jam", "syrup", "cheese", "pickle", "olives"]
    if any(kw in name for kw in micro_keywords): return "micro"
    if any(kw in name for kw in modest_keywords): return "modest"
    return "bulk"

# === Tag builder
def build_tags(ing):
    name = ing["Food Name"].strip().lower()
    p = val("Protein \n(g)", ing) or 0
    f = val("Fat, total \n(g)", ing) or 0
    c = val("Available carbohydrate, without sugar alcohols \n(g)", ing) or 0
    fiber = val("Total dietary fibre \n(g)", ing) or 0
    try:
        energy_kj = float(str(ing.get("Energy, without dietary fibre, equated \n(kJ)", "0")).replace(",", "").strip())
    except:
        energy_kj = 0
    kcal = round(energy_kj / 4.184, 2)

    tags = {
        "categoryTags": [],
        "dietaryTags": [],
        "nutritionTags": [],
        "cuisineTags": []
    }

    if any(w in name for w in ["chicken", "beef", "pork", "lamb", "fish", "egg", "salmon", "turkey", "ham", "yogurt", "cheese"]):
        tags["categoryTags"].append("animal_proteins")
    if any(w in name for w in ["tofu", "tempeh", "lentil", "bean", "chickpea", "falafel"]):
        tags["categoryTags"].append("plant_proteins")
    if any(w in name for w in ["rice", "potato", "bread", "pasta", "quinoa", "oats", "grain"]):
        tags["categoryTags"].append("starchy_carbs")
    if any(w in name for w in ["spinach", "kale", "zucchini", "tomato", "onion", "carrot", "pepper", "broccoli"]):
        tags["categoryTags"].append("non_starchy_veg")
    if any(w in name for w in ["oil", "avocado", "almond", "peanut", "seed", "butter", "nuts", "sunflower"]):
        tags["categoryTags"].append("healthy_fats")
    if any(w in name for w in ["garlic", "lemon", "vinegar", "chili", "spice", "ginger", "mustard"]):
        tags["categoryTags"].append("flavor_bases")
    if any(w in name for w in ["sauce", "dressing", "salsa", "gravy", "yogurt"]):
        tags["categoryTags"].append("sauces")
    if any(w in name for w in ["herb", "parsley", "cilantro", "flake", "seed", "crunch", "pickle"]):
        tags["categoryTags"].append("toppings")

    if any(w in name for w in ["milk", "yogurt", "cheese", "whey", "cream"]):
        tags["dietaryTags"].append("dairy")
    if any(w in name for w in ["bread", "pasta", "flour", "wheat", "crackers"]):
        tags["dietaryTags"].append("gluten")
    if any(w in name for w in ["almond", "walnut", "cashew", "peanut", "hazelnut"]):
        tags["dietaryTags"].append("nut")
    if any(w in name for w in ["soy", "tofu", "tempeh"]):
        tags["dietaryTags"].append("soy")
    if any(w in name for w in ["bean", "lentil", "chickpea", "pea"]):
        tags["dietaryTags"].append("legume")
    if any(w in name for w in ["chicken", "beef", "pork", "lamb", "fish", "egg", "salmon", "turkey", "ham", "yogurt", "cheese"]):
        tags["dietaryTags"].append("non_vegan")

    if p >= 8: tags["nutritionTags"].append("high_protein")
    if f <= 3: tags["nutritionTags"].append("low_fat")
    if f >= 15: tags["nutritionTags"].append("high_fat")
    if c <= 5: tags["nutritionTags"].append("low_carb")
    if fiber >= 4: tags["nutritionTags"].append("high_fiber")
    if (val("Calcium (Ca) \n(mg)", ing) or 0) >= 100: tags["nutritionTags"].append("high_calcium")
    if (val("Magnesium (Mg) \n(mg)", ing) or 0) >= 40: tags["nutritionTags"].append("high_magnesium")
    if (val("Choline \n(mg)", ing) or 0) >= 50: tags["nutritionTags"].append("high_choline")
    if (val("Iron (Fe) \n(mg)", ing) or 0) >= 2: tags["nutritionTags"].append("high_iron")
    if kcal > 0 and (p / kcal) >= 0.2 and p >= 8: tags["nutritionTags"].append("lean_protein_source")

    return tags

# === Field selector + cleaner
def assign_and_filter(ing):
    name = ing["Food Name"].strip()
    kcal = round((val("Energy, without dietary fibre, equated \n(kJ)", ing) or 0) / 4.184, 2)

    out = {
        "name": name,
        "kcal": kcal,
        "protein_g": val("Protein \n(g)", ing),
        "fat_g": val("Fat, total \n(g)", ing),
        "carbs_g": val("Available carbohydrate, without sugar alcohols \n(g)", ing),
        "fiber_g": val("Total dietary fibre \n(g)", ing),
        "calcium_mg": val("Calcium (Ca) \n(mg)", ing),
        "iron_mg": val("Iron (Fe) \n(mg)", ing),
        "magnesium_mg": val("Magnesium (Mg) \n(mg)", ing),
        "zinc_mg": val("Zinc (Zn) \n(mg)", ing),
        "copper_mg": val("Copper (Cu) \n(mg)", ing),
        "manganese_mg": val("Manganese (Mn) \n(mg)", ing),
        "selenium_ug": val("Selenium (Se) \n(ug)", ing),
        "vitamin_a_rae_ug": val("Vitamin A retinol equivalents \n(ug)", ing),
        "vitamin_c_mg": val("Vitamin C \n(mg)", ing),
        "vitamin_d_IU": (val("Vitamin D3 equivalents \n(ug)", ing) or 0) * 40,
        "vitamin_e_mg": val("Vitamin E \n(mg)", ing),
        "vitamin_k_ug": val("Vitamin K \n(ug)", ing) or val("Phylloquinone (vitamin K1) \n(ug)", ing),
        "thiamin_mg": val("Thiamin (B1) \n(mg)", ing),
        "riboflavin_mg": val("Riboflavin (B2) \n(mg)", ing),
        "niacin_mg": val("Niacin (B3) \n(mg)", ing),
        "vitamin_b6_mg": val("Pyridoxine (B6) \n(mg)", ing),
        "folate_total_ug": val("Total folates \n(ug)", ing),
        "vitamin_b12_ug": val("Cobalamin (B12) \n(ug)", ing),
        "pantothenic_acid_mg": val("Pantothenic acid (B5) \n(mg)", ing),
        "choline_mg": val("Choline \n(mg)", ing),
        "tags": build_tags(ing),
        "usage_weight_class": infer_usage_weight_class(name)
    }

    # Final cleanup: remove null or empty
    return {k: v for k, v in out.items() if k in KEEP_FIELDS and v not in [None, "", []]}

# === Apply logic
tagged = [assign_and_filter(ing) for ing in data if ing.get("Food Name")]

# === Export
with open("foundation_ingredients_nuttab_TAGGED_CLEAN.json", "w") as f:
    json.dump(tagged, f, indent=2)
