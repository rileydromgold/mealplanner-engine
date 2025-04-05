# src/template_selector.py

import json
from pathlib import Path
from collections import defaultdict
import random

def load_template_json(path):
    with open(path, 'r') as f:
        return json.load(f)

# Map of dietary restrictions → tags that should be excluded
DIETARY_EXCLUSIONS = {
    "vegan": ["contains_dairy", "contains_eggs", "contains_meat", "contains_fish"],
    "vegetarian": ["contains_meat", "contains_fish"],
    "dairy_free": ["contains_dairy"],
    "gluten_free": ["contains_gluten"],
    "nut_free": ["contains_nuts"],
    "soy_free": ["contains_soy"]
}

def get_dietary_exclusion_tags(required_tags):
    exclusions = set()
    for tag in required_tags.get("dietaryTags", []):
        exclusions.update(DIETARY_EXCLUSIONS.get(tag, []))
    return exclusions

def matches_required_tags(tmpl, required_tags):
    # Hard filter for dietary exclusions
    tmpl_diet_tags = set(tmpl.get("dietaryTags", []))
    exclusions = get_dietary_exclusion_tags(required_tags)
    if tmpl_diet_tags & exclusions:
        return False

    # Apply other required tags normally
    for tag_group, required_list in required_tags.items():
        if tag_group == "dietaryTags":
            continue  # already handled
        if not any(tag in tmpl.get(tag_group, []) for tag in required_list):
            return False
    return True

def score_preferred_tags(tmpl, preferred_tags, cuisine_prefs=None):
    score = 0
    for tag_group, preferred_list in preferred_tags.items():
        score += sum(1 for tag in preferred_list if tag in tmpl.get(tag_group, []))

    if cuisine_prefs:
        score += sum(1 for tag in cuisine_prefs if tag in tmpl.get("cuisineTags", []))

    return score

def build_template_pool(templates):
    pool = defaultdict(list)
    for tmpl in templates:
        for meal_type in tmpl.get("meal_types", []):
            pool[meal_type].append(tmpl)
    return pool

def select_templates(tag_filters, cuisine_prefs, template_path, templates_per_type=2, debug=False):
    templates = load_template_json(template_path)
    pool = build_template_pool(templates)
    used_templates = set()

    required_tags = tag_filters.get("requiredTags", {})
    preferred_tags = tag_filters.get("preferredTags", {})

    selected = {}
    for meal_type, candidates in pool.items():
        valid = [t for t in candidates if matches_required_tags(t, required_tags)]
        scored = [(t, score_preferred_tags(t, preferred_tags, cuisine_prefs)) for t in valid if t["id"] not in used_templates]

        # Sort by score and shuffle ties
        random.shuffle(scored)
        scored.sort(key=lambda x: x[1], reverse=True)

        final = [t[0] for t in scored[:templates_per_type]]

        # If not enough, fallback
        if len(final) < templates_per_type:
            fallback = [t for t in candidates if t["id"] not in used_templates and t not in final]
            random.shuffle(fallback)
            final += fallback[:templates_per_type - len(final)]

        selected[meal_type] = [t["id"] for t in final]
        used_templates.update(selected[meal_type])

    return {
        "selected_templates": selected,
        "template_pool": pool if debug else None
    }

# === Example run ===
if __name__ == "__main__":
    from simulation_engine import build_user_analysis

    def extract_tag_filters(input_data):
        return input_data.get("tag_filters", {})

    user = build_user_analysis(
        user_id="demo123",
        input_path=Path("data/raw/default_input_layer.json")
    )

    results = select_templates(
        tag_filters=extract_tag_filters(user["input_layer"]),
        cuisine_prefs=user["input_layer"].get("cuisine_prefs", []),
        template_path=Path("docs/meal_templates_tagged.json"),
        debug=False
    )

    print(json.dumps(results, indent=2))
