Meal Plan Generation System - Flow Overview

1. Analyze Requirements

- Pull relevant tags based on default_input_layer.json to use for later queries:
  e.g.
  • Dietary: vegan, high_protein, high_cal, low_cal
  • Cost: expensive, cheap
  • Nutrition: high vitamin C
  • Cuisine Prefs (now supported)
  • Prep Prefs (coming in future)

- Pull meal plan structure requirements
  a) Daily meal structure: e.g. Four; Breakfast, Lunch, Dinner, Snack  
  b) Variety: e.g 2 different types of each meal  
  c) Weekly Adherence: e.g. 6 out of 7  
  a*b = total number of meal templates or recipes required (in this example 8)  
  a*c = total number of meals for the week (24)
  

2. Select Meal Templates (Foundation-First + Hybrid Tag Matching)
- Choose templates that fulfill:
  • Meal structure (from input layer)
  • Required `dietaryTags` (hard-filtered)
  • Preferred `nutritionTags` and `cuisine_prefs` (soft scoring)

- Use `meal_templates_tagged.json` for candidate pool:
  e.g.
  • Breakfast: oat_bowl + breakfast_plate  
  • Lunch: grain_bowl + wrap_or_sandwich  
  • Dinner: stir_fry + tray_bake  
  • Snack: yogurt_bowl + snack_generic

- Selected templates support multiple `cuisineVariants`
- Cuisine assignment is handled **after selection**:
  • Lunch/Dinner: prioritize matching a user cuisine pref  
  • Breakfast/Snack: default to `"global"` if applicable  
- Prompt user for confirmation (in interface layer). If yes, move to step 3. If no, reroll candidates.

3. Populate Required Fields (Macro Foundation Phase)
- For each meal:
  • Assign rough quantities for `required` and `required_one_of` fields  
  • Match ingredient slots by `categoryTags` (e.g. animal_proteins, starchy_carbs, non_starchy_veg)  
  • Calculate per-meal macro targets using meal plan totals:  
    e.g. if daily target = 170g P / 65g F / 240g C → divide by # meals/day  
  • Target ~85% of total macros (leave room for patching layer)
  • Validate nutrition (≥85% of macros + calories)  
  • Generate nutrition report + patch requirements

4. Fetch Nutrition Patch Requirements (Micronutrient Fill Phase)
- For each meal:
  • Fill `optional` fields (sauces, toppings, flavor_bases, non_starchy_veg)  
  • Use matching `nutritionTags` and `cuisineTags` to prefer ingredients  
  • Validate post-patch nutrition (close to 100% of targets)  
  • Generate nutrition report, flag any outstanding deficiencies

5. Output
- Print proposed meals
- Generate nutrition report
- Show ingredient list and prep instructions
- Ready for user export or reroll

-------

### FLESHED OUT (Internal Execution Notes)

for step 1:
- User nutrition requirements are parsed from the input layer (e.g. `default_input_layer.json`)  
- Tags are extracted into `requiredTags` and `preferredTags` for selection logic  
- Weekly meal plan structure is defined (e.g. 6 days x 4 meals/day = 24 meal slots)

for step 2:
- Templates are selected based on hard filtering (`requiredTags` like `vegan`)  
- Soft preferences (like `high_protein` or `cuisine_prefs`) are scored  
- Resulting templates are matched to available cuisine variants *after selection*  
- This supports flexible structural meals (e.g. grain_bowl → latin, mediterranean, global)

for step 3:
- Calculate macro target per meal:  
  Daily macros = 170g protein, 65g fat, 240g carbs  
  Daily meals = 4  
  = 42.5g protein, 16.25g fat, 60g carbs per meal  
  → Apply 85% factor for foundational target:  
  = 36.1g protein, 13.8g fat, 51g carbs per meal

- Search ingredient pool (`foundation_ingredients_nuttab_TAGGED.json`) to populate slots by category
- Build and validate the macro base of each meal

step 4:
- Fill optional fields using ingredients that match missing micros or overall balance  
- Use `cuisineProfile` logic to guide optional ingredient selection  
- Final patch layer fills micronutrient gaps without breaking dietary prefs or cuisine cohesion

step 5:
- Output: meal schedule, ingredients, macros/micros, batch prep instructions  
- Optionally export to JSON, PDF, or user dashboard

