# src/simulation_engine.py

import json
from pathlib import Path

def load_input_layer(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def calculate_meal_plan_structure(input_data):
    structure = input_data.get("meal_structure", {})
    days = structure.get("days_per_week", 6)
    meals = structure.get("daily_meals", [])
    meals_per_day = sum(meal.get("frequency", 1) for meal in meals)
    unique_templates_required = meals_per_day * structure.get("variety_multiplier", 2)
    total_meal_slots = meals_per_day * days
    return {
        "days": days,
        "meals_per_day": meals_per_day,
        "unique_templates_required": unique_templates_required,
        "total_meal_slots": total_meal_slots
    }

def extract_tag_filters(input_data):
    return input_data.get("tag_filters", {})

def build_user_analysis(user_id, input_path):
    input_data = load_input_layer(input_path)
    plan_structure = calculate_meal_plan_structure(input_data)

    return {
        "user_id": user_id,
        "input_layer": input_data,
        "tag_filters": extract_tag_filters(input_data),
        "plan_structure": plan_structure
    }

# === Example run ===
if __name__ == "__main__":
    result = build_user_analysis(
        user_id="demo123",
        input_path=Path("data/raw/default_input_layer.json")
    )
    print(json.dumps(result, indent=2))
