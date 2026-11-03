from recommendation_engine import (
    food,
    filter_foods,
    select_diverse_food,
    calculate_serving_size
)


def generate_recommendations(daily_protein, daily_carbs, daily_fats):

    recommendations = {
        "Protein": [],
        "Carbohydrates": [],
        "Fat": []
    }

    # 1. Protein Recommendations

    avail_proteins = filter_foods(food, allowed_clusters=[4, 5])

    sel_proteins = select_diverse_food(
        avail_proteins,
        pool_size=150,
        num_items=3
    )

    if sel_proteins is not None:

        target_per_protein = round(daily_protein / 3, 1)

        for i in range(len(sel_proteins)):

            row = sel_proteins.iloc[[i]]

            portion = calculate_serving_size(
                row,
                target_per_protein,
                "Protein (g per 100g)"
            )

            recommendations["Protein"].append({
                "food": str(row['food'].values[0]),
                "serving": portion,
                "macro": target_per_protein
            })


    # 2. Carbohydrate Recommendations

    avail_carbs = filter_foods(food, allowed_clusters=[1, 7])

    sel_carbs = select_diverse_food(
        avail_carbs,
        pool_size=150,
        num_items=2
    )

    if sel_carbs is not None:

        target_per_carb = round(daily_carbs / 2, 1)

        for i in range(len(sel_carbs)):

            row = sel_carbs.iloc[[i]]

            portion = calculate_serving_size(
                row,
                target_per_carb,
                "Carbohydrates (g per 100g)"
            )

            recommendations["Carbohydrates"].append({
                "food": str(row['food'].values[0]),
                "serving": portion,
                "macro": target_per_carb
            })


    # 3. Fat Recommendations

    avail_fats = filter_foods(
        food,
        allowed_clusters=[3],
        preparation_state="raw"
    )

    sel_fats = select_diverse_food(
        avail_fats,
        pool_size=150,
        num_items=2
    )

    if sel_fats is not None:

        target_per_fat = round(daily_fats / 2, 1)

        for i in range(len(sel_fats)):

            row = sel_fats.iloc[[i]]

            portion = calculate_serving_size(
                row,
                target_per_fat,
                "Fat (g per 100g)"
            )

            recommendations["Fat"].append({
                "food": str(row['food'].values[0]),
                "serving": portion,
                "macro": target_per_fat
            })

    return recommendations