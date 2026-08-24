import pandas as pd
food = pd.read_csv('clustered_food_database.csv')

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