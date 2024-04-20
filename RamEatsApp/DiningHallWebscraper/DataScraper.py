# This file is a recreation of the Jupyter Notebook

#Scraper Imports
import requests, json, re
from bs4 import BeautifulSoup

#initialize supabase
from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

#Scrape Data
url = "https://dining.unc.edu/locations/chase/"
data = requests.get(url)
html = data.text

soup = BeautifulSoup(html, "html.parser")

active_meal = soup.find("div", {"class": "c-tab is-active"})

active_menu_stations = active_meal.find_all("div", {"class": "menu-station"})

menu_stations = []
final_cleaned_data = []

for station in active_menu_stations:
    station_menu_items = []
    station_items = station.find_all("li", {"class": "menu-item-li"}) # Finds each food item at the current station
    for dish in station_items:
        current_dish = {}
        current_dish[dish.find("a").text] = dish.find("a")['data-recipe']
        station_menu_items.append(current_dish)
        final_cleaned_data.append({"Name": dish.find("a").text, "StationName": station.find("h4").text})
    menu_stations.append({station.find("h4").text: station_menu_items})

recipes = []

# This code sucks and runs at n^4 need to fix LOL
for station in menu_stations:
    for item in station.values():
        for dish in item:
            for key in dish:
                url = "https://dining.unc.edu/wp-content/themes/nmc_dining/ajax-content/recipe.php?recipe=" + dish[key]
                recipes.append(url)

soups = []

for link in recipes:
    data = requests.get(link).text
    soups.append(data)

html_recipes = []

for entry in soups:
    # Parse the JSON string
    data = json.loads(entry)

    # Access the value associated with the 'html' key
    html_value = data.get('html')
    
    soup = BeautifulSoup(html_value, "html.parser")

    html_recipes.append(soup)

# Loop over every menu item
all_soups = []
all_item_names = []
text_output = []

for current_soup in html_recipes:
    output = current_soup.find_all("th")
    all_item_names.append(current_soup.find("h2").text)
    for item in output:
        text_output.append(re.split('(\d.+)', item.text.replace(" ", "").replace("\n", ""))[0:2])
    all_soups.append(text_output)  # Appends the item nutrition array to the list of all items

for items in all_soups: # all item nutrition lists
    output_dict = {}
    all_nutrition_lists = []
    final_output = {}
    for entry in items:
        try:
            output_dict[entry[0]] = entry[1]
            all_nutrition_lists.append(output_dict)
        except:
            all_nutrition_lists.append("error")
    x = 0
    for item_name in all_item_names:
        final_output[item_name] = all_nutrition_lists[x]
        x += 1

format_lst = []

#Format data for supabase
for i in final_output:
    sub_dict = {}
    sub_dict['Name'] = i
    for j in final_output[i]:
        if j == 'Calories' or j == 'TotalFat' or j == 'TotalCarbohydrate' or j == 'Protein':
            #strips non-numeric characters
            sub_dict[j] = int(re.sub(r'\D', '', str(final_output[i][j])))

    format_lst.append(sub_dict)

for i in format_lst:
    supabase.table('Menu').insert(i).execute()