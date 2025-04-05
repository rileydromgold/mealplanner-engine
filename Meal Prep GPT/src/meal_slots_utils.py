# src/meal_slots_utils.py

import random


def assign_planned_cuisine(template, user_cuisine_prefs, meal_type):
    cuisine_tags = template.get("cuisineTags", [])

    # If template has no cuisine tags, it's neutral
    if not cuisine_tags:
        return None

    # Only enforce preferences for lunch/dinner
    if meal_type in ["lunch", "dinner"]:
        matching = [c for c in cuisine_tags if c in user_cuisine_prefs]
        if matching:
            return random.choice(matching)
        else:
            return None  # fallback to null if no match
    else:
        # For breakfast/snack, assign any available cuisineTag or fallback to null
        return random.choice(cuisine_tags) if cuisine_tags else None


def generate_meal_slots(selected_templates, template_lookup, plan_structure, cuisine_prefs):
    """
    selected_templates: dict of {meal_type: [template_ids]}
    template_lookup: dict of {template_id: template_data}
    plan_structure: dict with `days`, `meals_per_day`, `total_meal_slots`
    cuisine_prefs: list of user's preferred cuisines
    """

    slots = []
    for meal_type, template_ids in selected_templates.items():
        for tid in template_ids:
            tmpl = template_lookup[tid]
            cuisine = assign_planned_cuisine(tmpl, cuisine_prefs, meal_type)
            slots.append({
                "meal_type": meal_type,
                "template_id": tid,
                "planned_cuisine": cuisine
            })
    return slots


# === Example run ===
if __name__ == "__main__":
    from simulation_engine import build_user_analysis
    from template_selector import select_templates
    from pathlib import Path
    import json

    user = build_user_analysis(
        user_id="demo123",
        input_path=Path("data/raw/default_input_layer.json")
    )

    selection = select_templates(
        tag_filters=user["tag_filters"],
        template_path=Path("data/processed/meal_templates_tagged.json"),
        templates_per_type=2
    )

    slots = generate_meal_slots(
        selected_templates=selection["selected_templates"],
        template_lookup=selection["template_lookup"],
        plan_structure=user["plan_structure"],
        cuisine_prefs=user["input_layer"]["cuisine_prefs"]
    )

    print(json.dumps(slots, indent=2))
