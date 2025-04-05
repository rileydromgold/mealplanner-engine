# src/generate_meal_slots.py

import json
from pathlib import Path
from simulation_engine import build_user_analysis
from template_selector import select_templates


def assign_cuisine_to_template(tmpl, meal_type, cuisine_prefs):
    allowed = tmpl.get("cuisineVariants", [])

    if meal_type in ["lunch", "dinner"]:
        for pref in cuisine_prefs:
            if pref in allowed:
                return pref
    elif meal_type in ["breakfast", "snack"]:
        if "global" in allowed:
            return "global"

    return None  # fallback


def generate_meal_slots(user):
    tag_filters = user["input_layer"].get("tag_filters", {})
    cuisine_prefs = user["input_layer"].get("cuisine_prefs", [])
    meal_structure = user["input_layer"].get("meal_structure", {})
    template_path = Path("data/processed/meal_templates_tagged.json")

    selection = select_templates(
        tag_filters=tag_filters,
        cuisine_prefs=cuisine_prefs,
        template_path=template_path,
        debug=True  # 🛠️ enable full template_pool output
    )

    slots = []
    for meal_def in meal_structure.get("daily_meals", []):
        meal_type = meal_def["meal_type"]
        freq = meal_def.get("frequency", 1)
        selected_templates = selection["selected_templates"].get(meal_type, [])

        for i in range(freq * meal_structure.get("variety_multiplier", 2)):
            tmpl_id = selected_templates[i % len(selected_templates)]
            tmpl_obj = next(
                (t for t in selection["template_pool"].get(meal_type, []) if t["id"] == tmpl_id),
                {}
            )
            planned_cuisine = assign_cuisine_to_template(tmpl_obj, meal_type, cuisine_prefs)
            slots.append({
                "meal_type": meal_type,
                "template_id": tmpl_id,
                "planned_cuisine": planned_cuisine
            })

    return slots


# === Example run ===
if __name__ == "__main__":
    user = build_user_analysis(
        user_id="demo123",
        input_path=Path("data/raw/default_input_layer.json")
    )
    results = generate_meal_slots(user)
    print(json.dumps(results, indent=2))
