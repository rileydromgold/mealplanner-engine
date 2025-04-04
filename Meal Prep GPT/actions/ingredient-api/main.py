from fastapi import FastAPI, Query
from typing import Optional
import json

# Load ingredient data once
with open("foundation_ingredients_nuttab_TAGGED.json", "r") as f:
    INGREDIENTS = json.load(f)

app = FastAPI()

@app.get("/ingredients")
def get_ingredients(
    q: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 20
):
    results = INGREDIENTS

    if q:
        results = [i for i in results if q.lower() in i["name"].lower()]

    if tags:
        tag_list = tags.split(",")
        results = [
            i for i in results if any(
                tag in (
                    i.get("tags", {}).get("categoryTags", []) +
                    i.get("tags", {}).get("nutritionTags", []) +
                    i.get("tags", {}).get("dietaryTags", []) +
                    i.get("tags", {}).get("cuisineTags", [])
                )
                for tag in tag_list
            )
        ]

    return results[:limit]
