
Meal Plan Generation System - Flow Overview

1. Analyze Requirements

- Pull relevant tags based on default_input_layer.json to use for later queries:
  e.g.
  • Dietary: vegan, high_protein, high_cal, low_cal
  • Cost: expensive, cheap
  • Nutrition: high vitamin C
  • Cuisine Prefs (coming in future)
  • Prep Prefs (coming in future)

- Pull meal plan structure requirements
  a) Daily meal structure: e.g. Four; Breakfast, Lunch, Dinner, Snack
  b) Variety: e.g 2 different types of each meal
  c) Weekly Adherence: e.g. 6 out of 7
  a*b = total number of meal templates or recipes required (in this example 8)
  a*c = total number of meals for the week (24)
  

2. Select Meal Templates
- Choose templates that fulfill meal plan structure and tags. Pull from meal_templates_tagged.yaml:
  e.g.
  • Breakfast: oat_bowl + breakfast_plate
  • Lunch: grain_bowl + wrap_or_sandwich
  • Dinner: stir_fry + tray_bake
  • Snack: yogurt_bowl + snack_generic

- Assign cuisine type to meal_templates that need assigning (in this case grain_bowl, wrap_or_sandwich, stir_fry, tray_bake)
- Prompt user for confirmation. If yes move to step 3, if no select different template that still fulfills meal plan structure and tags.


3. Populate Required Fields
- For each meal:
  • Assign rough quantities for required_one_of or required fields
  • Find required_one_of or required fields (usually animal_proteins, vegetable_proteins, starchy_carbs and non_starchy_veg )
  • Fill these fields using foundation_ingredients_nuttab_TAGGED.json, searching for matching categoryTags
  • Generate nutrition report
  • Validate nutrition (≥85% macro and calorie targets as specified in default_input_layer.json)
  • Flag issues: coverage problems, missing micronutrients
  • Generate nutrition patch requirements


4. Fetch Nutrition Patch Requirements
- For each meal:
  • find optional fields (usually sauces, toppings, flavor_bases and non_starchy_veg)
  • Fill these fields using foundation_ingredients_nuttab_TAGGED.json, searching for matching categoryTags, nutritionTags and cuisineTags
  • Generate post-patch nutrition report
  • Validate nutrition (roughly 100% macro, micro and calories)
  • Flag issues: coverage problems, missing micronutrients
  • Generate nutrition patch requirements

5. Output
- Print proposed meals
- Generate nutrition report
