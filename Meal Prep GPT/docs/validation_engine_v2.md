
# 🧠 Validation Engine v2 – Foundation-Pair Anchored Simulation

This replaces the old ingredient-first simulation logic with a **meal-anchored architecture**. Each meal is built from a realistic `protein + starch` combo, with embedded cuisine identity and ingredient reuse.

---

## 🎯 Overall Goal
Generate a weekly meal plan that:
- Hits macro targets (±5% kcal, ≥ protein, ≤ fat)
- Covers micronutrient RDIs (≥ 90% weekly average)
- Stays within budget
- Uses reusable, prep-safe ingredients
- Builds meals with cultural realism and flavor cohesion
- Is template-compatible

---

## 🧱 Phase-by-Phase Simulation

### 🔹 Phase 0: Load Constraints + Data
- Load user targets:
  - `calorie_target`
  - `protein_target`
  - `fat_limit`
  - `budget_max`
- Load external datasets:
  - `foundation_pairs.json` (protein + starch → cuisine)
  - Tagged ingredient list (from Cloud API)

**Debug Hook:**
- Log loaded values + number of available ingredients + anchor pair count
- Continue even if one source fails (warn, fallback to defaults)

---

### 🔹 Phase 1: Select 4–6 Anchor Pairs
Score each `protein + starch` pair on:
- Macro efficiency (can help hit protein and kcal goals)
- Micronutrient density (indirect via associated cuisine)
- Ingredient overlap potential (reuse score)
- Cuisine diversity (flavor variety)

Select 4–6 high-ranking anchors.

**Debug Hook:**
- Output chosen pairs, scores, and why others were skipped
- If scoring fails, fall back to manual list of diverse pairs

---

### 🔹 Phase 2: Simulate Meal Coverage
For each anchor pair:
- Select 1–2 real recipes with cuisine tag
- Pull required ingredients from Cloud API
- Assign portion sizes to approximate macro targets
- Build up weekly totals

Validate:
- Total kcal ±5%
- Total protein ≥ target
- Total fat ≤ limit
- Ingredient reuse score

**Debug Hook:**
- Log meal totals + per-anchor macros + unused anchors
- If one meal fails to load or balance, skip it and continue

---

### 🔹 Phase 3: Patch Micronutrient Gaps
- Simulate full week’s micronutrient totals
- Identify any vitamins/minerals < 90% RDI
- Add 2–4 patch ingredients that:
  - Fit existing cuisines
  - Are sub-100g and cost-efficient
  - Don’t violate macros or budget

**Debug Hook:**
- List nutrients patched, patch ingredients added
- If patching fails (no slot, no space), mark gaps but continue

---

### 🔹 Phase 4: Validate Final Plan
Final check:
- Macro compliance (hard targets)
- Micros ≥ 90% average (flex targets)
- Budget hit
- Every ingredient used ≥2x or pantry
- All meals fit allowed templates

**Debug Hook:**
- Report pass/fail for each axis
- Tag problematic meals or ingredients for review

---

### 🔹 Phase 5: Lock Plan
- Freeze selected ingredients and meals
- Output passes to meal generation engine

**Debug Hook:**
- Save all intermediate data structures to log or file
- Tag version of engine used for traceability

---

## 🧪 Debug Mode System
Every phase must:
- Catch and report failures or inconsistencies
- Skip gracefully to next phase unless plan is invalidated
- Log state (inputs + outputs) per phase for troubleshooting

Use structured debug objects:
```json
{
  "phase": "Phase 3",
  "status": "partial_success",
  "issues": ["Could not add iodine-rich patch ingredient"],
  "fallbacks_triggered": true
}
```

---

## 🔁 Notes
- Foundation pairs are the root of the plan
- No ingredients or meals are selected before anchors
- Patching is contextual and cuisine-aware
- Debug mode is always active in development mode
