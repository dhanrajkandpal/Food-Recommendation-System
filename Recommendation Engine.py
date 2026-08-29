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
    filtered_food = filtered_food[~filtered_food['food'].str.contains('liver|lungs|kidney|heart', case=False)]
    sorted_food = filtered_food.sort_values(by='micronutrient_density', ascending=False)

    return sorted_food


def select_diverse_food(sorted_food, pool_size=20):
    """
    Takes the density-sorted dataframe, isolates the top N healthiest options,
    and randomly selects one to ensure daily meal plan variety.
    """
    actual_pool_size = min(pool_size, len(sorted_food))

    if actual_pool_size == 0:
        return None

    # Isolate the top tier, then pick one randomly
    selected_item = sorted_food.head(actual_pool_size).sample(n=1)

    return selected_item