
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




------- FLESHED OUT MORE -------

so looking at this, in the backend we should be generating a live file that has,
for step 1:
- user nutrition requirements as inputted (this will basically just create a unique version of the default_input_layer.json i.e. userid6969_input_layer.json)
- input layer analyzed and relevant tags pulled from those requirements for future querying of the data base
- we call upon the user we call upon the input layer for the weekly meal plan structure, creating slots we must fill with meals from the meal_templates file. 
>> This part should be relatively easy

for step 2:
- we take the input layer info (meal plan structure+cuisine prefs+dietary prefs) and create a pool of candidates by querying the meal templates for certain tags, for example if the input layer includes a cuisine pref for latin cuisine we will preferentially pick meals that have that tag. Once the candidates have been filtered by tags it is fed to the AI, it basically says here are the requirements and here are the options, do your thing.

for step 3: We start ingredient populating the meal templates to meet high level requirements from the input layer (calories and macro split) however we only want to fill around 85% of the totals as we will get the other 15% in the micronutrient patching phase.
So we take the meal templates and calculate roughly how many macros we need for each template. This will require some math and logic, the most basic form would look something like this:
Daily macros = 170g protein, 65g fat, 240g carbs
Daily meals = 4 
Macros per meal = daily total divided by 4
= 42.5g protein, 16.25g fat, 60g carbs 
Daily Calories = 2300
Calories per meal = daily total divided by 4
= 575 cals 

Take this per meal totals and multiply by 0.85
Adjusted macros per meal = 36.125g protein, 13.8125g fat, 51g carbs
Adjusted calories per meal = 488.75

So somehow, and i havent quite figured this out yet, we need to search the ingredient list to match required fields (e.g. animal_proteins + starchy_carbs + non_starchy_veg)

Lets just leave it here for now knowing we need to do the micronutrient patching layer next but this is a big enough task on its own.
