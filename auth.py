from flask import Blueprint, redirect, request, url_for, session, render_template, jsonify
import requests
from flask_login import login_user, logout_user, login_required
from oauthlib.oauth2 import WebApplicationClient
from user import User
from db import get_cursor, close_connection
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

def get_google_provider_cfg():
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    return requests.get(GOOGLE_DISCOVERY_URL).json()

#Login with oauth
@auth_bp.route('/login')
def login():
    #Builds oauth request and sends request
    client = WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID'))
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)

#Checks if login credentials are valid
@auth_bp.route('/login_trad', methods=['POST'])
def login_trad():
    #Retrieves form information from front end
    data = request.get_json()
    #If json data is not none
    if data:
        email = data.get('email')
        password = data.get('password')
        user = get_user_by_email(email)

        #If login information is valid
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            print("success login info")
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    return jsonify({'success': False, 'message': 'Invalid request'}), 400

#Retrieves user from the database by their email
def get_user_by_email(email):
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, name, email, profile_pic, password_hash FROM User WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        if user_data:
            return User(id_=user_data[0], name=user_data[1], email=user_data[2], profile_pic=user_data[3], password_hash=user_data[4])
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        close_connection(conn)

#Account creation 
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #Gets new account information from front end
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if not get_user_by_email(email):
            if User.create_user(name, email, hashed_password):
                #Returns back to app.py file in map function
                return redirect('/')
        else:
            print("Email already exists")
            #Refresh the page
            return render_template('auth/signup.html', error="Email already exists.")
    return render_template('signup.html')

#Not sure what this does. Source of current error (maybe).
@auth_bp.route('/login/callback')
def callback():
    code = request.args.get("code")
    client = WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID'))
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.getenv('GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_SECRET'))
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

        user = User(id_=unique_id, name=users_name, email=users_email, profile_pic=picture, password_hash=None)
        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email, picture, None)
        login_user(user)

        return redirect(url_for("map"))
    else:
        return "User email not available or not verified by Google.", 400

#Go back to login page
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    print("Session keys after logout:", session.keys()) 
    return redirect('/displayLogin')
