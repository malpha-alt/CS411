from flask import Flask, render_template, request, jsonify, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from auth import auth_bp
from user import User
import requests
import json
import db
from friends import friends_bp
from maps import maps_bp

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
db.init_app(app)
load_dotenv() #Loads the .env file
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(friends_bp)
app.register_blueprint(maps_bp)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')


#Retrieves database information
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=0)  # Immediately expire

#Blueprints


#Connects to mysql
mysql = MySQL()
mysql.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # type: ignore


#Loads current user if logged in
@login_manager.user_loader
def load_user(id):
     user = User.get(id)
     return user

#If not logged in, display login page
@app.route("/displayLogin")
def displayLogin():
    return render_template('login.html')

#Main page of website (Shows the map)
@app.route('/')
def map():
    if current_user.is_authenticated:
        #Get concertList from the database
        conn, cursor = db.get_cursor()
        cursor.execute("SELECT search_data FROM UserSearches WHERE userID = %s", (current_user.id,))
        user_searches = cursor.fetchall()
      
        #Add database information to a list to send to map creation
        concert_list = []
        for search in user_searches:
            results = json.loads(search[0])
            concert_list.extend(results)
        cursor.close()
        conn.close()

        #Builds the api call
        mapCall = 'https://maps.googleapis.com/maps/api/js?key=' + os.getenv('GOOGLE_MAP_API') + '&callback=initMap' # type: ignore
        return render_template('googleMap.html', mapCall=mapCall, concertList=concert_list)
    else:
        #If not logged in go to login page
        return render_template('login.html')
    
#Adds the selected concert to the database
@app.route('/storedata', methods=['POST']) 
@login_required
def storedata():
    try:
        data = request.get_json() #Retrieve data from front end
        id = current_user.id
        concertList = json.dumps(data)
        conn, cursor = db.get_cursor()

        #Executes a mysql command
        cursor.execute(
            "INSERT INTO UserSearches (userID, search_data) VALUES (%s, %s)",
            (id, concertList)
        )
        conn.commit()
        conn.close()
        cursor.close()
                
        return jsonify({'message': 'Data stored successfully'}), 200
    except Exception as e:
        #Error in storing data
        app.logger.error(f"Error storing data: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500

#Loads the setlist.fm api headers
api_key = os.getenv('SETLIST_API_KEY')
headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
}

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    artist = request.form.get('query') # Result from search bar
    date = request.form.get('date') #Result from date

    results = []
    #Checks if information was entered for both artist and date
    if artist and date: 
        #Formats form date into query param format
        date_object = datetime.strptime(date, '%Y-%m-%d')
        date = date_object.strftime('%d-%m-%Y')

        #Form query paramaters and build api call
        query_params = {"artistName": artist, 
                        "date": date}  
        endpoint = "https://api.setlist.fm/rest/1.0/search/setlists"
        response = requests.get(endpoint, params=query_params, headers=headers).json()
        
        #If the response is not None
        if response.get("setlist"): 
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
    app.run(host='127.0.0.1', port=5000, debug=True)