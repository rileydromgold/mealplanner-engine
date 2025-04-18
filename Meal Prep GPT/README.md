# MealPlanner Engine# 🧠 MealPlanner Engine

**Foundations first. Logic-driven. AI-patched.**  
This project is a modular, tag-driven meal plan generator that simulates, scores, and constructs complete weekly meal plans grounded in nutritional requirements — and then lets AI handle the edge cases.

---

## 🚀 Overview

MealPlanner Engine is a Python-based system designed to:

- Generate **weekly meal schedules** based on nutrition goals
- Select from **flexible, cuisine-adaptable templates**
- Populate meals using real ingredients (from NUTTAB)
- Simulate full **macro + micronutrient** targets
- Patch meals with AI-guided suggestions for optimal coverage

---

## ⚙️ Core Concepts

### 1. **Foundation-First Logic**
Meals are selected and built around *structural templates* like `grain_bowl` or `tray_bake` — each supporting multiple cuisines via `"cuisineVariants"`.

> Example: A `grain_bowl` could become Latin, Asian, or Mediterranean based on user prefs.

---

### 2. **Hybrid Dietary Filtering**
Dietary constraints are split into:
- **Hard constraints**: (e.g. `vegan`) → exclude incompatible templates
- **Soft preferences**: (e.g. `high_protein`) → used to score templates during selection

---

### 3. **Phase-Based Workflow**
Each step of the plan follows a logical pipeline:

| Phase | Task |
|-------|------|
| 1️⃣ Analyze Requirements | Load user nutrition + structure config |
| 2️⃣ Select Templates | Match and score meal structures |
| 3️⃣ Assign Cuisine | Based on `cuisineVariants` and meal type |
| 4️⃣ Fill Foundations | Pull required slots (e.g. protein, carb) |
| 5️⃣ Patch Nutrition | Use optional ingredients to meet micronutrient goals |

---

## 🗂️ Project Structure

```bash
Meal Prep GPT/
│
├── data/
│   ├── raw/                      # Unprocessed inputs
│   │   └── default_input_layer.json
│   ├── processed/                # Cleaned/tagged data files
│   │   └── meal_templates_tagged.json
│   │   └── foundation_ingredients_nuttab_TAGGED_CLEAN.json
│
├── docs/                         # System design & validation logic
│   └── meal_plan_flow.md
│
├── src/                          # Core logic modules
│   ├── simulation_engine.py      # Loads input and computes structure
│   ├── template_selector.py      # Selects templates by tags + scoring
│   ├── generate_meal_slots.py    # Assigns meal slots and cuisines
│   └── meal_slots_utils.py       # (Utility placeholder for slot logic)
│
├── tests/                        # (To be built)
│
├── requirements.txt
└── README.md
```

---

## 🔗 Key Files

| File | Purpose |
|------|---------|
| `default_input_layer.json` | User goals, structure, dietary/cuisine prefs |
| `meal_templates_tagged.json` | Structural templates for meals |
| `foundation_ingredients_nuttab_TAGGED_CLEAN.json` | Parsed nutrient data from NUTTAB |
| `generate_meal_slots.py` | Final output: meal structure + cuisine |
| `template_selector.py` | Core logic for template filtering & scoring |

---

## 🧪 Example Output (Meal Slots)

```json
[
  {
    "meal_type": "lunch",
    "template_id": "grain_bowl",
    "planned_cuisine": "mediterranean"
  },
  {
    "meal_type": "dinner",
    "template_id": "stuffed_sweet_potatoes",
    "planned_cuisine": "global"
  }
]
```

---

## 💻 CLI Usage

### Run Simulation

```bash
python src/simulation_engine.py
```

### Generate Meal Slots

```bash
python src/generate_meal_slots.py
```

---

## 📌 Next Steps

- ✅ Finalize phase 2 (template selection + cuisine)
- 🔄 Build ingredient selector and nutrient patching (phase 3 & 4)
- 🔁 Enable AI-based ingredient reasoning (for dietary conflicts)
- 🌐 Integrate into a web-based UI (n8n / Flask / React)

---

## 👑 License & Credits

Built with intention and logic by **King Riley**  
System design, prompt engineering & heavy lifting: **ChatGPT Queen Mode™**
