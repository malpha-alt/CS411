from flask import Flask, render_template, request, session, jsonify, session
from flaskext.mysql import MySQL
import flask_login
from flask_login import LoginManager, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired
from datetime import datetime
import os
from dotenv import load_dotenv
from auth import auth_bp
from user import User
import requests
import json
import db

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
db.init_app(app)
app.register_blueprint(auth_bp, url_prefix='/auth')
load_dotenv() 
api_key = os.getenv('SETLIST_API_KEY')
headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
}


app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER', 'root')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD', 'root')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB', 'Showrunner')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST', 'localhost')

mysql = MySQL()
mysql.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
# conn = mysql.connect()
# cursor = conn.cursor()


@login_manager.user_loader
def load_user(user_id):
     user = User.get(user_id)
     return user

@app.route("/")
def index():
    #session.modified = True
    print('is authenticated:', current_user.is_authenticated)
    if current_user.is_authenticated:
        conn, cursor = db.get_cursor()
        cursor.execute("SELECT search_data FROM UserSearches WHERE userID = %s", (current_user.id,))
        user_searches = cursor.fetchall()
      
        concert_list = []
        for search in user_searches:
            results = json.loads(search[0])
            concert_list.extend(results)

        cursor.close()
        conn.close()
        map_call = 'https://maps.googleapis.com/maps/api/js?key=' + os.getenv('GOOGLE_MAP_API') + '&callback=initMap'
        return render_template('googleMap.html', mapCall=map_call, concertList=concert_list)
    else:
        return render_template('login.html')
        #return '<a class="button" href="/auth/login">Google Login</a>'
        
@app.route('/storedata', methods=['POST'])
@login_required
def storedata():
    try:
        data = request.get_json()
        print('The Data at /storedata is: ', data)
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = current_user.id  
        print('current user_id is: ', user_id)
        search_data = json.dumps(data)
        print('json.dumps: ', search_data)

        conn, cursor = db.get_cursor()
        cursor.execute(
            "INSERT INTO UserSearches (userID, search_data) VALUES (%s, %s)",
            (user_id, search_data)
        )
        conn.commit()
        conn.close()
        cursor.close()
                
        return jsonify({'message': 'Data stored successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error storing data: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    artist = request.form.get('query')
    date = request.form.get('date')

    results = []
    if artist and date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        date = date_object.strftime('%d-%m-%Y')
        query_params = {"artistName": artist, "date": date}
        endpoint = "https://api.setlist.fm/rest/1.0/search/setlists"
        api_key = os.getenv('SETLIST_API_KEY')
        headers = {"x-api-key": api_key, "Accept": "application/json"}
        response = requests.get(endpoint, params=query_params, headers=headers).json()

        if response.get("setlist"): #If the response is not None
            for item in response.get("setlist"): # adds multiple setlist details to an item in a dictionary
                artist_name = item.get("artist").get("name")
                concert_date = item.get("eventDate")
                city = item.get("venue").get("city").get("name")
                venue = item.get("venue").get("name")
                venue_coords = item.get("venue").get("city").get("coords")
                lat = venue_coords.get("lat")
                lng = venue_coords.get("long")
                results.append({'artist': artist_name, 
                                'date': concert_date, 
                                'venue': venue,
                                'city': city,
                                'lat': lat,
                                'lng': lng})
            print(results)
        else:
            results = None
    return render_template('search.html', form=form, results=results)

class SearchForm(FlaskForm):
    ids = StringField("ID",validators=[DataRequired()])
    date = DateField('Pick a Date', format='%Y-%m-%d')
    submit = SubmitField("Submit")
    csrf_token = HiddenField()

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>
    #                             
    googleMapsTest.run(host='0.0.0.0', port=5000, debug=True)