import json

menu = [
    {"Name": "Southwest Style Sirloin", "Calories": 240, "Protein": 26, "TotalCarbohydrate": 10, "TotalFat": 8, "healthiness": 9},
    {"Name": "Steamed Whole Green Beans", "Calories": 35, "Protein": 2, "TotalCarbohydrate": 8, "TotalFat": 0, "healthiness": 7},
    {"Name": "Rice Blend", "Calories": 160, "Protein": 3, "TotalCarbohydrate": 31, "TotalFat": 2, "healthiness": 7},
    {"Name": "Roasted Cauliflower", "Calories": 60, "Protein": 2, "TotalCarbohydrate": 7, "TotalFat": 2, "healthiness": 7}
]

def calculate_meals(menu):
    # Sort menu items by calories (ascending order)
    sorted_menu = sorted(menu, key=lambda x: x["Calories"])

    # Define meal and macronutrient goals
    meal_cal = 2500
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
        if total_calories + info["Calories"] <= meal_cal_upper:
            # Check if adding this item exceeds macronutrient limits
            if ((total_protein + info["Protein"]) / meal_cal_upper) <= protein_goal \
                and ((total_carbs + info["TotalCarbohydrate"]) / meal_cal_upper) <= carbs_goal \
                and ((total_fats + info["TotalFat"]) / meal_cal_upper) <= fats_goal:

                # Adjust serving size if needed to fill meal calories within bounds
                remaining_calories = meal_cal_upper - total_calories
                portion = 1.0  # Default portion is the whole item
                if info["Calories"] > remaining_calories:
                    if info["Calories"] >= 0.5 * remaining_calories:
                        portion = 0.5
                    elif info["Calories"] >= 2.0 * remaining_calories:
                        portion = 2.0

                # Add adjusted item to the selected list
                selected_items.append((info["Name"], portion))
                total_calories += info["Calories"] * portion
                total_protein += info["Protein"] * portion
                total_carbs += info["TotalCarbohydrate"] * portion
                total_fats += info["TotalFat"] * portion

        else:
            break  # Stop adding items if the next item would exceed the calorie limit

    # Check if there are remaining calories to prioritize items with more protein
    remaining_calories = meal_cal_upper - total_calories
    if remaining_calories > 0:
        sorted_items = sorted(selected_items, key=lambda x: next(item for item in menu if item["Name"] == x[0])["Protein"], reverse=True)
        for item, portion in sorted_items:
            if remaining_calories >= next(info for info in menu if info["Name"] == item)["Calories"]:
                # Find the item in the selected_items list and update its portion
                for i, (selected_item, selected_portion) in enumerate(selected_items):
                    if selected_item == item:
                        selected_items[i] = (selected_item, selected_portion + 1.0)
                        total_calories += next(info for info in menu if info["Name"] == item)["Calories"]
                        total_protein += next(info for info in menu if info["Name"] == item)["Protein"]
                        total_carbs += next(info for info in menu if info["Name"] == item)["TotalCarbohydrate"]
                        total_fats += next(info for info in menu if info["Name"] == item)["TotalFat"]
                        remaining_calories -= next(info for info in menu if info["Name"] == item)["Calories"]
                        break

    # Adjust total calories to be within the specified upper and lower bounds
    if total_calories > meal_cal_upper:
        excess_calories = total_calories - meal_cal_upper
        for i, (item, portion) in enumerate(selected_items):
            item_calories = next(info for info in menu if info["Name"] == item)["Calories"] * portion
            if item_calories >= excess_calories:
                # Reduce the portion of this item
                reduction = excess_calories / next(info for info in menu if info["Name"] == item)["Calories"]
                selected_items[i] = (item, portion - reduction)
                total_calories -= excess_calories
                break
            else:
                # Remove this item entirely
                excess_calories -= item_calories
                total_calories -= item_calories
                selected_items[i] = (item, 0)

    elif total_calories < meal_cal_lower:
        shortfall_calories = meal_cal_lower - total_calories
        for i, (item, portion) in enumerate(selected_items):
            item_calories = next(info for info in menu if info["Name"] == item)["Calories"] * portion
            if item_calories <= shortfall_calories:
                # Increase the portion of this item
                increase = shortfall_calories / next(info for info in menu if info["Name"] == item)["Calories"]
                selected_items[i] = (item, portion + increase)
                total_calories += shortfall_calories
                break

    # Truncate long decimals and cast to nearest whole integer
    selected_items = [(item, int(portion)) if portion.is_integer() else (item, round(portion)) for item, portion in selected_items]

    return selected_items, total_calories, total_protein, total_carbs, total_fats


print(calculate_meals(menu))