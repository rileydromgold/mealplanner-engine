import json

# === CONFIG ===
INPUT_FILE = "foundationDownload.json"
OUTPUT_FILE = "foundation_ingredients.json"

# === Map of nutrient ID → (category, field_name)
nutrient_map = {
    # Macros
    "203": ("macros_per_100g", "protein_g"),
    "204": ("macros_per_100g", "fat_g"),
    "205": ("macros_per_100g", "carbs_g"),
    "208": ("macros_per_100g", "calories_kcal"),
    "291": ("macros_per_100g", "fiber_g"),
    "269": ("macros_per_100g", "sugars_g"),

    # Micros
    "301": ("micros", "calcium_mg"),
    "303": ("micros", "iron_mg"),
    "304": ("micros", "magnesium_mg"),
    "305": ("micros", "phosphorus_mg"),
    "306": ("micros", "potassium_mg"),
    "307": ("micros", "sodium_mg"),
    "309": ("micros", "zinc_mg"),
    "312": ("micros", "copper_mg"),
    "315": ("micros", "manganese_mg"),
    "317": ("micros", "selenium_ug"),
    "320": ("micros", "vitamin_a_rae_ug"),
    "401": ("micros", "vitamin_c_mg"),
    "324": ("micros", "vitamin_d_IU"),
    "323": ("micros", "vitamin_e_mg"),
    "430": ("micros", "vitamin_k_ug"),
    "404": ("micros", "thiamin_mg"),
    "405": ("micros", "riboflavin_mg"),
    "406": ("micros", "niacin_mg"),
    "415": ("micros", "vitamin_b6_mg"),
    "417": ("micros", "folate_total_ug"),
    "418": ("micros", "vitamin_b12_ug"),
    "410": ("micros", "pantothenic_acid_mg"),
    "421": ("micros", "choline_mg"),

    # Lipids
    "606": ("lipids", "saturated_fat_g"),
    "645": ("lipids", "monounsaturated_fat_g"),
    "646": ("lipids", "polyunsaturated_fat_g"),
    "605": ("lipids", "trans_fat_g"),
    "601": ("lipids", "cholesterol_mg"),
    "851": ("lipids", "omega_3_g"),
    "852": ("lipids", "omega_6_g"),

    # Aminos
    "501": ("aminos_per_100g", "tryptophan_g"),
    "502": ("aminos_per_100g", "threonine_g"),
    "503": ("aminos_per_100g", "isoleucine_g"),
    "504": ("aminos_per_100g", "leucine_g"),
    "505": ("aminos_per_100g", "lysine_g"),
    "506": ("aminos_per_100g", "methionine_g"),
    "507": ("aminos_per_100g", "cystine_g"),
    "508": ("aminos_per_100g", "phenylalanine_g"),
    "509": ("aminos_per_100g", "tyrosine_g"),
    "510": ("aminos_per_100g", "valine_g"),
    "511": ("aminos_per_100g", "arginine_g"),
    "512": ("aminos_per_100g", "histidine_g"),
    "513": ("aminos_per_100g", "alanine_g"),
    "514": ("aminos_per_100g", "aspartic_acid_g"),
    "515": ("aminos_per_100g", "glutamic_acid_g"),
    "516": ("aminos_per_100g", "glycine_g"),
    "517": ("aminos_per_100g", "proline_g"),
    "518": ("aminos_per_100g", "serine_g")
}

# === Load the USDA Foundation file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# If file starts with {"FoundationFoods": [...]}, unwrap it:
foods = data["FoundationFoods"] if "FoundationFoods" in data else data

results = []

for food in foods:
    entry = {
        "name": food.get("description"),
        "fdcId": food.get("fdcId"),
        "measurement_basis": "raw",
        "macros_per_100g": {},
        "micros": {},
        "lipids": {},
        "aminos_per_100g": {}
    }

    for nutrient in food.get("foodNutrients", []):
        nutrient_info = nutrient.get("nutrient", {})
        nid = str(nutrient_info.get("number"))
        amount = nutrient.get("amount")

        if nid in nutrient_map and amount is not None:
            section, field = nutrient_map[nid]
            entry[section][field] = amount

    results.append(entry)

# === Save to output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"✅ Extracted {len(results)} items with mapped nutrients to {OUTPUT_FILE}")
