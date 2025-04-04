# File: validation_engine.md
# 🧠 Validation Engine Logic

The simulation engine powers the core planning logic that ensures macro, micro, cost, and prep constraints are all met before generating meals.

---

## Phase 1: Macro-First Allocation (85% Calories)
- Select prep-friendly, reusable, cost-aware ingredients
- Hit `calorie_target`, `protein_target`, and `fat_limit`
- Prioritize batch-cooking and template compatibility

Output: `macro_ingredient_pool`

---

## Phase 2: Micronutrient Simulation
- Aggregate micro values × planned portions × 6 days
- Compare to weekly RDI targets
- Flag each nutrient:
  - ✅ ≥100% → Covered
  - ⚠️ 75–99% → Partial
  - ❌ <60% → Deficient

**Non-blocking** → diagnostics only.

---

## Phase 3: Patch Layer (15% Calories)
- Add 2–4 ingredients targeting flagged deficiencies
- Must:
  - Fit budget
  - Fit templates
  - Avoid excessive calorie inflation

Fallbacks:
- Sub ingredient if critical nutrient missing
- Downgrade expensive boosters

---

## Phase 4: Final Validation
Check:
- Calories = ±5%
- Protein + Fat = targets hit
- Micronutrients = all ✅ or ⚠️
- Cost = within budget
- Reuse = all non-pantry ingredients used ≥2x

Raise:
- Missing nutrients
- Budget overflows
- Template gaps
Suggest:
- Targeted swaps
- Drop/replace logic
- Add bump food (e.g., oats, rice)

---

## Phase 5: Lock Plan
Freeze pool → pass to meal generation.
No new foods unless substitution required.
