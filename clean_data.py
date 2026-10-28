import re
import ray
import pandas as pd

def clean_batch(batch: dict) -> dict:
    cleaned_recipes = []

    for recipe in batch["ingredients"]:
        cleaned_recipe = []
        for ing in recipe:
            text = ing.lower()
            text = re.sub(r"[^a-z\s]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            
            if text:
                cleaned_recipe.append(text)
                
        cleaned_recipes.append(cleaned_recipe)

    batch["ingredients"] = cleaned_recipes
    return batch

def clean_dataset(input_path: str, output_path: str):
    ds = ray.data.read_json(input_path)
    cleaned_ds = ds.map_batches(clean_batch)

    df = cleaned_ds.to_pandas()

    df["ingredients"] = [list(x) for x in df["ingredients"]]
    
    df.to_parquet(output_path, index=False)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)
    clean_dataset("data/train.json", "data/train_cleaned.parquet")
    clean_dataset("data/test.json", "data/test_cleaned.parquet")