# 🧠 Validation Engine v3 – Template-Driven Simulation

This defines the logic used to generate a full weekly meal plan based on structured inputs, pulling from tagged templates and ingredients.

---

## 🎯 Goal
Generate a plan that:
- Hits macro targets (±5% kcal, ≥ protein, ≤ fat)
- Covers ≥90% weekly micronutrient RDIs
- Stays within budget
- Reuses ingredients
- Uses real, prep-safe meals from known templates

---

## 🧱 Simulation Flow

### 🔹 Phase 0: Load Inputs
- Load user constraints from `default_input_layer.json`:
  - `calorie_target`, `protein_target`, `fat_limit`, `budget_max`
  - `meal_structure.days` and `meal_structure.meals_per_day`
  - `tags` (dietary, nutrition, cost)
- Load `meal_templates_tagged.yaml`
- Load tagged ingredients from Cloud API (`foundation_ingredients_nuttab_TAGGED.json`)

**Debug:**
```json
{
  "phase": "Phase 0",
  "status": "loaded",
  "calorie_target": 2700,
  "tags_applied": ["high_protein", "dairy_free"],
  "meal_structure": {"breakfast": 2, "lunch": 2, "dinner": 2, "snack": 2},
  "fallback_to_defaults": false
}
```

---

### 🔹 Phase 1: Select Meal Templates
- For each meal type (e.g. breakfast, lunch, etc), select N templates
- Filter by:
  - `meal_types` field in template
  - Tags matching user profile
- Assign `cuisineTag` (manual or inferred)
- Prompt user to confirm template and cuisine selection

**Debug:**
```json
{
  "phase": "Phase 1",
  "meal_type": "lunch",
  "candidates": ["grain_bowl", "wrap"],
  "selected_templates": ["grain_bowl", "wrap"],
  "cuisineTags": ["mediterranean", "mexican"],
  "fallback_to_default_cuisine": false
}
```

---

### 🔹 Phase 2: Build Nutrition Foundations
For each selected template:
- Fill all `required` and `required_one_of` slots using:
  - Matching `categoryTags` from ingredient dataset
  - Filter by `cuisineTag` if available, else fallback to global match
- Estimate meal portion sizes
- Track and log selected ingredient pool with quantities, including full macro and micronutrient data sourced directly from `foundation_ingredients_nuttab_TAGGED.json`
- Simulate macros and calories
- Validate ≥85% macro and calorie coverage
- Generate interim report of per-meal coverage and flagged gaps

**Debug:**
```json
{
  "phase": "Phase 2",
  "template": "grain_bowl",
  "slots_filled": ["animal_protein", "starchy_carbs", "non_starchy_veg"],
  "estimated_kcal": 610,
  "macro_coverage": 87,
  "fallback_triggered": false
}
```

---

### 🔹 Phase 3: Patch + Enrich Meals
- Fill optional fields (`sauces`, `toppings`, `flavor_bases`, `extra_veg`)
- Filter by `cuisineTag`, `nutritionTags`, and gaps
- Pull additional ingredients from database and assign estimated weights
- Retry patching until full macro + micro targets are approximated
- Re-run full nutrition validation post-patch (100% target aim)

**Debug:**
```json
{
  "phase": "Phase 3",
  "meal": "grain_bowl",
  "patch_ingredients": ["lemon_juice", "tahini", "parsley"],
  "micronutrients_improved": ["iron", "vitamin C"],
  "final_macro": 95,
  "final_micro": 92,
  "loop_count": 2
}
```

---

### 🔹 Phase 4: Final Validation
Validate full weekly plan:
- Aggregate across `meal_structure.days`
- Confirm:
  - Macro targets met
  - Micros ≥90% RDI
  - Budget not exceeded
  - Ingredients reused ≥2× unless pantry
  - All templates used in correct meal type

**Debug:**
```json
{
  "phase": "Phase 4",
  "macro_ok": true,
  "micro_ok": true,
  "budget_ok": true,
  "reuse_violations": ["zucchini"],
  "invalid_templates": []
}
```

---

### 🔹 Phase 5: Output
- Finalize all meals
- Generate:
  - Meal schedule
  - Ingredient list with amounts
  - Batch prep instructions
  - Nutrition report:
    - Avg daily kcal
    - Avg macros
    - Micros as % of RDI

**Debug:**
```json
{
  "phase": "Phase 5",
  "meals_finalized": 24,
  "templates_used": ["oat_bowl", "smoothie", "grain_bowl", "wrap", "stir_fry", "tray_bake", "snack", "frittata"],
  "output_files": ["MealPlan_Week01_v1.json", "grocery_list.csv"]
}
```

---

## 🧪 Debug Mode
Always active in dev builds.
Logs inputs, outputs, fallbacks, and failure causes per phase.

```json
{
  "phase": "Phase 3",
  "status": "partial_success",
  "issues": ["Missing Vitamin D"],
  "fallbacks_triggered": true
}
```

---

## Notes
- Templates define structure
- Ingredient categories = `categoryTags`
- Cuisine tags steer flavor and coherence
- Fallbacks ensure graceful degradation