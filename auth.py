from flask import Blueprint, redirect, request, url_for, session
import requests
from flask_login import login_user, logout_user, login_required
from oauthlib.oauth2 import WebApplicationClient
from user import User
import os
import json

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

def get_google_provider_cfg():
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@auth_bp.route('/login')
def login():
    client = WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID'))
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)

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
        auth=(os.getenv('GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_SECRET')),
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

        user = User(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)
        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email, picture)
        login_user(user)

        return redirect(url_for("index"))
    else:
        return "User email not available or not verified by Google.", 400

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
