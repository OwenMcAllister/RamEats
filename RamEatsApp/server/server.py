from flask import Flask, request, jsonify #,session
from flask_cors import CORS
#from flask_session import Session
#from cachelib.file import FileSystemCache
from supabase import create_client
import os
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
#app.secret_key = "test"
#SESSION_TYPE = "cachelib"
#SESSION_SERIALIZATION_FORMAT = 'json'
#app.config['SESSION_CACHELIB'] = FileSystemCache(threshold=500, cache_dir="flask_session")
#app.config.from_object(__name__)
#Session(app)
CORS(app, supports_credentials=True)

session = {}


#initialize supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

#Backend route to receive data from frontent user authentication
@app.route('/api/auth', methods=['POST'])

def authenticate():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    action = data.get('action') #login or signup

    #process data
    if action == 'login':
        #login supabase action
        response = supabase.auth.sign_in_with_password({"email":email, "password":password})
        user_id = response.user.id
        session["user"] = str(user_id)

        user_data = supabase.table('Users').select('height').eq('uid', user_id).execute()
        
        if user_data.count == None:

            return jsonify({'redirect': '/onboarding/gender'})



    if action == 'signup':
        #create new supabase user    
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        user_id = response.user.id
        supabase.table('Users').insert({'uid': user_id}).execute()

        return jsonify({'redirect': '/login'})


#Backend route to receieve data during onboard process
@app.route('/api/onboard', methods=['POST'])

def onboard():

    if "user" not in session:
        return jsonify({'redirect': '/login'})
    
    user_id = session["user"]
    response = supabase.table('Users').select("*").eq('uid', user_id).execute()
    data = response.data
    row = data[0]
    
    data = request.json
    step = data.get('step') #activityLevel, fitnessGoal, height, sex, timeline, weight

    #data processing dependant on step in onboarding process

    if step == 'activityLevel':

        activity = data.get('activityLevel')

        #push data to supabase
        supabase.table('Users').update({"activityLevel": activity}).eq('uid', user_id).execute()

        #redirect
        return jsonify({'redirect': '/onboarding/fitgoals'})
        
    
    elif step == 'fitnessGoal':

        fitness = data.get('goal')

        #push data to supabase
        supabase.table('Users').update({"fitnessGoal": fitness}).eq('uid', user_id).execute()


    elif step == 'height':

        feet = data.get('feet')
        inches = data.get('inches')

        inchesTotal = int(feet) * 12 + int(inches)

        height = int(inchesTotal * 2.54)

        #push data to supabase
        supabase.table('Users').update({"height": height}).eq('uid', user_id).execute()

        #redirect to next step
        return jsonify({'redirect': '/onboarding/weight'})


    elif step == 'gender':

        gender = data.get('gender')

        #push data to supabase
        supabase.table('Users').update({"gender": gender}).eq('uid', user_id).execute()

        #Redirect to next step
        return jsonify({'redirect': '/onboarding/height'})


    elif step == 'timeLine':

        time = data.get('timeLine')

        #push data to supabase
        supabase.table('Users').insert({"timeLine": time}).execute()

    elif step == 'weight':

        lbs = data.get('weight')
        weight = int(int(lbs) * 0.453592)

        #push data to supabase
        supabase.table('Users').update({"weight": weight}).eq('uid', user_id).execute()

        #redirect to next step
        return jsonify({'redirect': '/onboarding/age'})

    elif step == 'age':
        age = data.get('age')

        #Push data to supabase
        supabase.table('Users').update({"age":age}).eq('uid', user_id).execute()

        #redirect
        return jsonify({'redirect': '/onboarding/activelevel'})


    #Calculate total kcal requirement and send to db

    response = supabase.table('Users').select("*").eq('uid', user_id).execute()
    data = response.data
    row = data[0]
    gender = row["gender"]
    weight = int(row["weight"])
    height = int(row["height"])
    age = int(row["age"])
    fitness = row["fitnessGoal"]
    activity = int(row["activityLevel"])
        
    bmr: int = 0 # basal metabolic rate variable
    result: int = 0

    # Calculates the BMR for Male and Female
    if gender == "Male":
        bmr = int((10 * weight) + (6.25 * height) - (5 * age) + 5)

    else:
        bmr = int((10 * weight) + (6.25 * height) - (5 * age) - 161)

    # Finds the daily calories needed for maintainance at a particular activity level
    result = int(bmr + activity)

    if fitness == ("gain"):
        result = int(result * 1.1)
        supabase.table('Users').update({'kcalTotal':result}).eq('uid', user_id).execute()
    
    elif fitness == ("lose"):
        result = int(result * .9)
        supabase.table('Users').update({'kcalTotal':result}).eq('uid', user_id).execute()

    else:
        supabase.table('Users').update({'kcalTotal':result}).eq('uid', user_id).execute()

    
    return jsonify({'redirect': '/'})



@app.route('/api/meal', methods=['GET'])

def calcMeals():

    if "user" not in session:
        return jsonify({'redirect': '/login'})

    #load user totKcal
    user_id = session["user"]
    response = supabase.table('Users').select("*").eq('uid', user_id).execute()
    data = response.data
    row = data[0]
    dailyTotCal = row["kcalTotal"]


    #load menu
    menu_data = supabase.table('Menu').select("*").execute()
    menu = menu_data.data

    # Get current time
    now = datetime.now()
    current_time = now.time()

    # Define time ranges for breakfast, lunch, and dinner
    breakfast_start = datetime.strptime('07:00:00', '%H:%M:%S').time()
    breakfast_end = datetime.strptime('10:45:00', '%H:%M:%S').time()

    lunch_start = datetime.strptime('11:00:00', '%H:%M:%S').time()
    lunch_end = datetime.strptime('14:00:00', '%H:%M:%S').time()

    dinner_start = datetime.strptime('17:00:00', '%H:%M:%S').time()
    dinner_end = datetime.strptime('20:00:00', '%H:%M:%S').time()

    menu_data = supabase.table('Menu').select("*").execute()
    menu = menu_data.data

    # Calculate Meal based on current time
    if breakfast_start <= current_time <= breakfast_end:
        menu = supabase.table('Menu').select('*').eq('The Kitchen Table').execute()
    elif lunch_start <= current_time <= lunch_end:
        menu = supabase.table('Menu').select('*').eq('Simply Prepared Grill').execute()
    elif dinner_start <= current_time <= dinner_end:
        menu = supabase.table('Menu').select('*').eq('Simply Prepared Grill').execute()


        # Sort menu items by calories (ascending order)
    sorted_menu = sorted(menu, key=lambda x: x["Calories"])

    # Define meal and macronutrient goals
    meal_cal = dailyTotCal
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
                selected_items[i] = (item, 0.0)

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

    # Return data as JSON
    result = {
        "selected_items": selected_items,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats
    }
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)