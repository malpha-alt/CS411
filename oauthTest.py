import json
import os
import sqlalchemy

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, redirect, request, url_for
from flask_login import(
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

from oauthlib.oauth2 import WebApplicationClient
import requests


GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)

GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content", 403

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            
            # "<p>Hello, {}. You're are logged into concert chronicles. Email: {}<\p>"
            # '<img src="{}" alt="Google profile pic"></img><div>'
            # '<a class=button" href="/logout">Logout</a>' .format(
            #     current_user.name, current_user.email, current_user.profile_pic
            # )
            '<a>You are logged in to concert chronicles!</a>'
        )
    else:
        return '<a class="button" href="/login">Login with Google account</a>'

@app.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://localhost:5000/login/callback",
        scope = ['openid', 'email', 'profile']
    )
    return redirect(request_uri)

@app.route('/loginSuccess')
def loginSuccess():
    return (
            
            # "<p>Hello, {}. You're are logged into concert chronicles. Email: {}<\p>"
            # '<img src="{}" alt="Google profile pic"></img><div>'
            # '<a class=button" href="/logout">Logout</a>' .format(
            #     current_user.name, current_user.email, current_user.profile_pic
            # )
            '<a>You are logged in to concert chronicles!</a>'
        )

@app.route('/login/callback')    
def callback():
    code = request.args.get('code')
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url,headers,body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET)
    )

    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri,headers,body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print(userinfo_response.json())

    if userinfo_response.json().get('email_verified'):
        unique_id = userinfo_response.json()['sub']
        users_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        users_name = userinfo_response.json()['given_name']
    else:
        return "User not verified by google", 400

    return redirect("/loginSuccess")

    user = User(
        id=unique_id, name=users_name,email=users_email,profile_pic=picture
    )

    # if not User.get(unique_id):
    #     User.create(unique_id, users_name,users_email,picture)

    login_user(user)

    return redirect("/")
    

def get_google_provider_cfg():
        return requests.get(GOOGLE_DISCOVERY_URL).json()    

if __name__ == '__main__':
    app.run(debug=True)



      