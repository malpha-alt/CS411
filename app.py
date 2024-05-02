from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user, login_required
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
from profileInfo import profile_bp

#Forces oauth to work on http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
db.init_app(app)
load_dotenv() #Loads the .env file
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(friends_bp)
app.register_blueprint(maps_bp)
app.register_blueprint(profile_bp, url_prefix='/profile')
app.config['SECRET_KEY'] = os.urandom(32)


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

concert_list = []

#Main page of website (Shows the map)
@app.route('/')
def map():
    if current_user.is_authenticated:
        #Get concertList from the database
        conn, cursor = db.get_cursor()
        cursor.execute("SELECT search_data FROM UserSearches WHERE userID = %s", (current_user.id))
        user_searches = cursor.fetchall()
        #Add database information to a list to send to map creation
        concert_list = []
        for search in user_searches:
            results = json.loads(search[0])
            concert_list.extend(results)
        cursor.close()
        conn.close()
        #Builds the api call
        mapCall = f"https://maps.googleapis.com/maps/api/js?key={os.getenv('GOOGLE_DEV_API')}&loading=async&callback=initMap"
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
        concert = json.dumps(data)
        conn, cursor = db.get_cursor()
        newConcert = json.loads(concert)[0]
        cursor.execute("SELECT search_data FROM UserSearches WHERE userID = %s", (current_user.id,))
        user_searches = cursor.fetchall()

        #If first user search insert into table
        if len(user_searches) == 0:
            cursor.execute(
                "INSERT INTO UserSearches (userID, search_data) VALUES (%s, %s)",
                (id, concert)
            )
            conn.commit()
            conn.close()
            cursor.close()
            return jsonify({'message': 'Data stored successfully'}), 200
        else:
            #Add database information to a list of concerts
            concert_list = []
            for search in user_searches:
                results = json.loads(search[0])
                concert_list.extend(results)
            #Checks for duplicate concerts
            if newConcert not in concert_list:
                concert_list.append(newConcert) 
                concert_list = json.dumps(concert_list) #Converts to json data
                cursor.execute(
                    "UPDATE UserSearches SET search_data = %s WHERE userID = %s", 
                    (concert_list, id)
                )
                conn.commit()
                conn.close()
                cursor.close()
                        
                return jsonify({'message': 'Data stored successfully'}), 200
            else: 
                return jsonify({'error': 'Concert already added'}), 500
    except Exception as e:
        #Error in storing data
        app.logger.error(f"Error storing data: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500

@app.route('/removeconcert', methods=['POST'])
@login_required
def removeConcert():
    try:
        data = request.get_json() #Retrieve data from front end
        id = current_user.id
        concert_to_remove = json.dumps(data)
        concert_to_remove = json.loads(concert_to_remove)[0]
        conn, cursor = db.get_cursor()
        cursor.execute("SELECT search_data FROM UserSearches WHERE userID = %s", (id))
        user_searches = cursor.fetchall()

        #Grabs all concerts from user_searches
        updated_concert_list = []
        for search in user_searches:
            results = json.loads(search[0])
            updated_concert_list.extend(results)

        updated_concert_list.remove(concert_to_remove) #Removes concert from list
        updated_concert_list = json.dumps(updated_concert_list) #Converts back to json
        #Updates the dp with the removed concert list
        cursor.execute(
            "UPDATE UserSearches SET search_data = %s WHERE userID = %s", 
            (updated_concert_list, id)
        )
        conn.commit()
        conn.close()
        cursor.close()
        return jsonify({'message': 'Data removed successfully'}), 200
    except Exception as e:
        #Error in storing data
        app.logger.error(f"Error removing data: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500


#Loads the setlist.fm api headers
api_key = os.getenv('SETLIST_API_KEY')
headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
}

@app.route('/search', methods=['GET', 'POST'])
def search():
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
                if len(item.get("sets").get("set")) > 0:
                    artist_name = item.get("artist").get("name")
                    concert_date = item.get("eventDate")
                    city = item.get("venue").get("city").get("name")
                    venueName = item.get("venue").get("name")
                    venueState = item.get("venue").get("city").get("stateCode")
                    venueCountry = item.get("venue").get("city").get("country").get("code")
                    address = f"{venueName}, {city}, {venueState}, {venueCountry}"
                    lat, lng = getVenueCoords(address, item.get("venue").get("city").get("lat"), item.get("venue").get("city").get("lng"))
                    setlist = []
                    songs = item.get("sets").get("set")[0].get("song")
                    for x in range (len(songs)):
                        setlist.append(songs[x].get("name"))
                    results.append({'artist': artist_name, 
                                'date': concert_date, 
                                'venue': venueName,
                                'city': city,
                                'state': venueState,
                                'country': venueCountry,
                                'lat': lat,
                                'lng': lng,
                                'set': setlist})
        else:
            results = None
    return jsonify(results)

#Gets coordinates by calling google geocoding
def getVenueCoords(address, defLat, defLng):
    apiKey = os.getenv('GOOGLE_DEV_API')
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={apiKey}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return defLat, defLng #Return city coordinates if venue coordinates could not be found
    else:
        print(f"HTTP GET Request failed with status code {response.status_code}")

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>      
    app.run(host='127.0.0.1', port=5000, debug=True)