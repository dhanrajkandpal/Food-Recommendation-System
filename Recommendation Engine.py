import pandas as pd
food = pd.read_csv('clustered_food_database.csv')
pd.set_option('display.max_columns', None)
lean_bulk_blueprint = {
    "protein_slots": 2,
    "protein_clusters": [4, 5],
    "carb_slots": 2,
    "carb_clusters": [1, 7],
    "fat_slots": 1,
    "fat_clusters": [2, 5],
    "volume_slots": 1,
    "volume_clusters": [0]
}
sustain_blueprint = {
    "protein_slots": 2,
    "protein_clusters": [4, 5],
    "carb_slots": 1,
    "carb_clusters": [1, 6],
    "fat_slots": 1,
    "fat_clusters": [3, 7],
    "volume_slots": 1,
    "volume_clusters": [0]
}
cut_blueprint = {
    "protein_slots": 2,
    "protein_clusters": [4, 5],
    "carb_slots": 1,
    "carb_clusters": [1, 6],
    "fat_slots": 1,
    "fat_clusters": [3, 7],
    "volume_slots": 1,
    "volume_clusters": [0]
}


def filter_foods(food, allowed_clusters, preparation_state="cooked"):
    """
    Filters the food database based on K-Means clusters and preparation state,
    then sorts by micronutrient density.
    """
    filtered_food = food[
        (food['clusters'].isin(allowed_clusters)) &
        (food['preparation'] == preparation_state)
        ].copy()
    # Gate 2.5: Filter out organ meats, brains, and exotic animals
    filtered_food = filtered_food[~filtered_food['food'].str.contains('liver|lungs|kidney|heart|spleen|splean|ostrich|brain', case=False)]
    sorted_food = filtered_food.sort_values(by='micronutrient_density', ascending=False)

    return sorted_food


def select_diverse_food(sorted_food, pool_size=150, num_items=1):
    """
    Takes the density-sorted dataframe, isolates the top N healthiest options,
    and randomly selects multiple distinct items to ensure daily variety.
    """
    actual_pool_size = min(pool_size, len(sorted_food))

    if actual_pool_size == 0:
        return None

    items_to_pull = min(num_items, actual_pool_size)
    selected_items = sorted_food.head(actual_pool_size).sample(n=items_to_pull)

    return selected_items

def calculate_serving_size(food_row, target_macro_grams, primary_macro):
    """
    Calculates the exact gram weight of a food needed to hit a specific macronutrient target.
    """
    macro_per_100g = food_row[primary_macro].values[0]
    if macro_per_100g == 0:
        return 0
    serving_grams = (target_macro_grams / macro_per_100g) * 100
    return round(serving_grams, 1)


def generate_daily_allowance(daily_protein, daily_carbs, daily_fats, protein_splits=3, carb_splits=2, fat_splits=2):
    """Generates a daily ingredient target list, splitting macros across multiple foods."""

    print("--- YOUR DAILY INGREDIENT ALLOWANCE ---")
    print("Cook these items and distribute them across your day however you prefer:\n")

    # 1. Source Daily Proteins
    avail_proteins = filter_foods(food, allowed_clusters=[4, 5])
    sel_proteins = select_diverse_food(avail_proteins, pool_size=150, num_items=protein_splits)
    target_per_protein = round(daily_protein / protein_splits, 1)

    print(f"PROTEINS (Total Target: {daily_protein}g)")
    for i in range(len(sel_proteins)):
        row = sel_proteins.iloc[[i]]
        portion = calculate_serving_size(row, target_per_protein, "Protein (g per 100g)")
        print(f"[ ] {portion}g of {row['food'].values[0]} (Yields {target_per_protein}g Protein)")
    print()

    # 2. Source Daily Carbs
    avail_carbs = filter_foods(food, allowed_clusters=[1, 7])
    sel_carbs = select_diverse_food(avail_carbs, pool_size=150, num_items=carb_splits)
    target_per_carb = round(daily_carbs / carb_splits, 1)

    print(f"CARBOHYDRATES (Total Target: {daily_carbs}g)")
    for i in range(len(sel_carbs)):
        row = sel_carbs.iloc[[i]]
        portion = calculate_serving_size(row, target_per_carb, "Carbohydrates (g per 100g)")
        print(f"[ ] {portion}g of {row['food'].values[0]} (Yields {target_per_carb}g Carbs)")
    print()

    # 3. Source Daily Fats
    avail_fats = filter_foods(food, allowed_clusters=[3], preparation_state="raw")
    sel_fats = select_diverse_food(avail_fats, pool_size=150, num_items=fat_splits)
    target_per_fat = round(daily_fats / fat_splits, 1)

    print(f"FATS (Total Target: {daily_fats}g)")
    for i in range(len(sel_fats)):
        row = sel_fats.iloc[[i]]
        portion = calculate_serving_size(row, target_per_fat, "Fat (g per 100g)")
        print(f"[ ] {portion}g of {row['food'].values[0]} (Yields {target_per_fat}g Fats)")
    print()