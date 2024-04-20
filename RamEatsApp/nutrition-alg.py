import json

menu = [
    {"Name": "Salad", "calories": 150, "protein": 5, "total carbohydrate": 10, "total fat": 8, "healthiness": 9},
    {"Name": "Grilled Chicken Sandwich", "calories": 300, "protein": 25, "total carbohydrate": 30, "total fat": 12, "healthiness": 7},
    {"Name": "Rice", "calories": 230, "protein": 5, "total carbohydrate": 300, "total fat": 2, "healthiness": 7}
]

def calculate_meals(menu):
    # Sort menu items by calories (ascending order)
    sorted_menu = sorted(menu, key=lambda x: x["calories"])

    # Define meal and macronutrient goals
    meal_cal = 1000
    meal_cal_lower = meal_cal - 50
    meal_cal_upper = meal_cal + 50
    protein_goal = 0.24 * meal_cal_upper
    carbs_goal = 0.53 * meal_cal_upper
    fats_goal = 0.23 * meal_cal_upper

    selected_items = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0

    for info in sorted_menu:
        if total_calories + info["calories"] <= meal_cal_upper:
            # Check if adding this item exceeds macronutrient limits
            if ((total_protein + info["protein"]) / meal_cal_upper) <= protein_goal \
                and ((total_carbs + info["total carbohydrate"]) / meal_cal_upper) <= carbs_goal \
                and ((total_fats + info["total fat"]) / meal_cal_upper) <= fats_goal:

                # Adjust serving size if needed to fill meal calories within bounds
                remaining_calories = meal_cal_upper - total_calories
                portion = 1.0  # Default portion is the whole item
                if info["calories"] > remaining_calories:
                    if info["calories"] >= 0.5 * remaining_calories:
                        portion = 0.5
                    elif info["calories"] >= 2.0 * remaining_calories:
                        portion = 2.0

                # Add adjusted item to the selected list
                selected_items.append((info["Name"], portion))
                total_calories += info["calories"] * portion
                total_protein += info["protein"] * portion
                total_carbs += info["total carbohydrate"] * portion
                total_fats += info["total fat"] * portion

        else:
            break  # Stop adding items if the next item would exceed the calorie limit

    # Check if there are remaining calories to prioritize items with more protein
    remaining_calories = meal_cal_upper - total_calories
    if remaining_calories > 0:
        sorted_items = sorted(selected_items, key=lambda x: next(item for item in menu if item["Name"] == x[0])["protein"], reverse=True)
        for item, portion in sorted_items:
            if remaining_calories >= next(info for info in menu if info["Name"] == item)["calories"]:
                # Find the item in the selected_items list and update its portion
                for i, (selected_item, selected_portion) in enumerate(selected_items):
                    if selected_item == item:
                        selected_items[i] = (selected_item, selected_portion + 1.0)
                        total_calories += next(info for info in menu if info["Name"] == item)["calories"]
                        total_protein += next(info for info in menu if info["Name"] == item)["protein"]
                        total_carbs += next(info for info in menu if info["Name"] == item)["total carbohydrate"]
                        total_fats += next(info for info in menu if info["Name"] == item)["total fat"]
                        remaining_calories -= next(info for info in menu if info["Name"] == item)["calories"]
                        break

    # Adjust total calories to be within the specified upper and lower bounds
    if total_calories > meal_cal_upper:
        excess_calories = total_calories - meal_cal_upper
        for i, (item, portion) in enumerate(selected_items):
            item_calories = next(info for info in menu if info["Name"] == item)["calories"] * portion
            if item_calories >= excess_calories:
                # Reduce the portion of this item
                reduction = excess_calories / next(info for info in menu if info["Name"] == item)["calories"]
                selected_items[i] = (item, portion - reduction)
                total_calories -= excess_calories
                break
            else:
                # Remove this item entirely
                excess_calories -= item_calories
                total_calories -= item_calories
                selected_items[i] = (item, 0.0)

    elif total_calories < meal_cal_lower:
        shortfall_calories = meal_cal_lower - total_calories
        for i, (item, portion) in enumerate(selected_items):
            item_calories = next(info for info in menu if info["Name"] == item)["calories"] * portion
            if item_calories <= shortfall_calories:
                # Increase the portion of this item
                increase = shortfall_calories / next(info for info in menu if info["Name"] == item)["calories"]
                selected_items[i] = (item, portion + increase)
                total_calories += shortfall_calories
                break

    return selected_items, total_calories, total_protein, total_carbs, total_fats

print(calculate_meals(menu))

# Return data as JSON
# result = {
#     "selected_items": selected_items,
#     "total_calories": total_calories,
#     "total_protein": total_protein,
#     "total_carbs": total_carbs,
#     "total_fats": total_fats
# }
# print(json.dumps(result))
