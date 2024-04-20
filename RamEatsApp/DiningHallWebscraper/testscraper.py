# Scraper Imports
import requests
import json
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client
import os

# Initialize Supabase
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# Define the table name in Supabase
table_name = "TestMenu"

# Clear existing data in the table (optional, remove if not needed)
supabase.table(table_name).delete().execute()

# Scrape Data
url = "https://dining.unc.edu/locations/chase/"
data = requests.get(url)
html = data.text
soup = BeautifulSoup(html, "html.parser")

active_meal = soup.find("div", {"class": "c-tab is-active"})
active_menu_stations = active_meal.find_all("div", {"class": "menu-station"})

menu_items = []

for station in active_menu_stations:
    station_name = station.find("h4").text.strip()
    station_items = station.find_all("li", {"class": "menu-item-li"})
    for item in station_items:
        item_name = item.find("a").text.strip()
        item_recipe = item.find("a")['data-recipe']
        menu_items.append({"Station": station_name, "Name": item_name, "Recipe": item_recipe})
        try:
            supabase.table(table_name).insert({"StationName": station_name}).execute()
        except:
            supabase.table(table_name).insert({"StationName": "None"}).execute()

recipes = []

for item in menu_items:
    url = "https://dining.unc.edu/wp-content/themes/nmc_dining/ajax-content/recipe.php?recipe=" + item["Recipe"]
    recipes.append(url)

soups = []

for link in recipes:
    data = requests.get(link).text
    soups.append(data)

html_recipes = []

for entry in soups:
    data = json.loads(entry)
    html_value = data.get('html')
    soup = BeautifulSoup(html_value, "html.parser")
    html_recipes.append(soup)

# Loop over every menu item
all_soups = []

for current_soup, item in zip(html_recipes, menu_items):
    station_name = item["Station"]
    item_name = item["Name"]
    nutrition_rows = current_soup.find_all("tr")
    item_nutrition = {}

    for row in nutrition_rows:
        columns = row.find_all("td")
        if len(columns) == 2:
            nutrient = columns[0].text.strip()
            value = columns[1].text.strip()
            item_nutrition[nutrient] = value

    all_soups.append({"Station": station_name, "Name": item_name, "Nutrition": item_nutrition})

# Format data for Supabase
formatted_data = []

for item in all_soups:
    formatted_item = {"Station": item["Station"], "Name": item["Name"]}
    nutrition_dict = item["Nutrition"]

    for nutrient in ["Calories", "TotalFat", "TotalCarbohydrate", "Protein"]:
        if nutrient in nutrition_dict:
            value = nutrition_dict[nutrient]
            numeric_value = int(re.sub(r'\D', '', value))  # Remove non-numeric characters
            formatted_item[nutrient] = numeric_value

    formatted_data.append(formatted_item)

# Insert data into Supabase
for item in formatted_data:
    supabase.table(table_name).insert(item).execute()
