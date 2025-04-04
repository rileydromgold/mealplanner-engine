# 🏷️ Tagging Rules for Ingredient Metadata

This document defines the logic used to assign metadata tags to ingredients in the `foundation_ingredients.json` file. These tags are grouped into structured categories and are used throughout the meal planning engine for filtering, validation, substitution, and generation.

---

## 📦 Tag Groups

### 1. `categoryTags`
Used to map ingredients to template slots.

| Tag | Description | Trigger Logic |
|-----|-------------|----------------|
| `animal_proteins` | Complete proteins from animal sources | name contains: chicken, beef, pork, lamb, fish, egg, salmon, turkey, ham, yogurt, cheese |
| `plant_proteins` | Protein + fiber sources from plants | name contains: tofu, tempeh, lentil, bean, chickpea, falafel |
| `starchy_carbs` | Primary calorie-dense carbs | name contains: rice, potato, bread, pasta, quinoa, oats, grain |
| `non_starchy_veg` | Low-carb, micronutrient-rich veg | name contains: spinach, kale, zucchini, tomato, onion, carrot, pepper, broccoli |
| `healthy_fats` | High-fat, nutrient-dense sources | name contains: oil, avocado, almond, peanut, seed, butter, nuts, sunflower |
| `flavor_bases` | Aromatics and acid sources | name contains: garlic, lemon, vinegar, chili, spice, ginger, mustard |
| `sauces` | Ingredients used as sauces or dressing | name contains: sauce, dressing, salsa, gravy, yogurt |
| `toppings` | Garnish or textural components | name contains: herb, parsley, cilantro, flake, seed, crunch, pickle |

### 2. `dietaryTags`
Used to filter ingredients based on user dietary preferences or restrictions.

| Tag | Trigger Logic |
|-----|---------------|
| `non_vegan` | animal product keywords in name |
| `dairy` | milk, yogurt, cheese, whey, cream in name |
| `gluten` | bread, pasta, flour, wheat, crackers in name |
| `nut` | almond, walnut, cashew, peanut, hazelnut in name |
| `soy` | soy, tofu, tempeh in name |
| `legume` | bean, lentil, chickpea, pea in name |

### 3. `nutritionTags`
Used for filtering high-value ingredients or for patching micronutrient gaps.

| Tag | Condition |
|-----|-----------|
| `high_protein` | protein_g ≥ 8 |
| `low_fat` | fat_g ≤ 3 |
| `high_fat` | fat_g ≥ 15 |
| `low_carb` | carbs_g ≤ 5 |
| `high_fiber` | fiber_g ≥ 4 |
| `high_calcium` | calcium_mg ≥ 100 |
| `high_magnesium` | magnesium_mg ≥ 40 |
| `high_choline` | choline_mg ≥ 50 |
| `high_iron` | iron_mg ≥ 2 |
| `lean_protein_source` | (protein_g / kcal) ≥ 0.20 and protein_g ≥ 8 |

Additionally, each ingredient is assigned a float value `protein_kcal_ratio = protein_g / kcal`

### 4. `cuisineTags`
Used to infer likely cuisines for flavor systems, grouping, and variation.

| Tag | Trigger Logic (name contains) |
|-----|-------------------------------|
| `indian` | paneer, dal, masoor, ghee |
| `latin` | chorizo, tortilla, tamale |
| `asian` | soy, tofu, miso, bok choy |
| `mediterranean` | yogurt, chickpea, feta, olive, parsley |
| `middle_eastern` | tahini, bulgur, lamb |
| `american` | turkey, cheddar, white bread, ground beef |
| `european` | rye, sausage, butter, cream |

---

## 🔍 Debugging & Audit Tips

- If an ingredient seems misclassified, check its name and macronutrient values.
- Use `protein_kcal_ratio` to determine if something marked `high_protein` is actually suitable as a core protein source.
- Multi-category tags (e.g. yogurt = `animal_proteins` + `sauces`) are expected and valid.

---

## 🛠 Planned Extensions

- `prepTags`: quick_cook, batch_friendly, shelf_stable
- `flavorProfileTags`: umami, earthy, acidic, smoky, sweet, nutty, etc.

