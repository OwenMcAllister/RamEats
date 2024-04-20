#TEST SCRIPT FOR RAPID DEV (random supabase testing only)

from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

def register(email, password):
    user = supabase.auth.sign_up({"email": email, "password": password})
    print(user)


def login(email, password):
    response = supabase.auth.sign_in_with_password({"email":email, "password":password})
    #session_token = response.response

login('owencmc@unc.edu','TestPass123')
session = supabase.auth.get_session()
user_id = session.user.id


menu_data = supabase.table('Menu').select("*").execute()
data = menu_data.data
menu = data

print(menu)