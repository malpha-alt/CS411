from flask import Flask, render_template, request, jsonify
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

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
db.init_app(app)
load_dotenv() #Loads the .env file
app.register_blueprint(auth_bp, url_prefix='/auth')
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')


#Retrieves database information
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=0)  # Immediately expire



#Connects to mysql
mysql = MySQL()
mysql.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # type: ignore


#Functions for getting emails/ids
def getUserIdFromEmail(email):
    conn, cursor = db.get_cursor()
    cursor.execute(
        "SELECT id FROM User WHERE email = '{0}'".format(email))
    return cursor.fetchone()[0]

def getUsersFriends(uid):
    conn, cursor = db.get_cursor()
    cursor.execute("SELECT id2 FROM Friends WHERE id1 = '{0}'".format(uid))
    return cursor.fetchall()

def isFriendsWith(uid, uid2):
    conn, cursor = db.get_cursor()
    print(uid)
    print(uid2)
    if cursor.execute("SELECT id2 FROM Friends WHERE id1 = {0} AND id2 = {1}".format(uid, uid2)):
        print(cursor.execute("SELECT id2 FROM Friends WHERE id1 = {0} AND id2 = {1}".format(uid, uid2)))
        return True
    else:
        return False

def getFirstNameFromId(id):
    conn, cursor = db.get_cursor()
    cursor.execute(
        "SELECT name  FROM User WHERE id = '{0}'".format(id))
    return cursor.fetchone()[0]

def getEmailFromId(id):
    conn, cursor = db.get_cursor()
    cursor.execute(
        "SELECT email FROM User WHERE id = '{0}'".format(id))
    return cursor.fetchone()[0]

def friendTuple(uid):
    friendIds = getUsersFriends(uid)
    friends = []
    for i in friendIds:
        friends.append((getFirstNameFromId(i[0]), getEmailFromId(i[0]), i[0]))
    return friends

def friendRecs(uid):
    friends = friendTuple(uid)
    #adds current user to friends list so the user isn't recommended to themself
    friends.append((getFirstNameFromId(uid), getEmailFromId(uid), uid))
    friendsOfFriends = set()
    for i in range(len(friends)):
        friendsOfCurrentUser = friendTuple(friends[i][2])
        for x in range(len(friendsOfCurrentUser)):
            friendsOfFriends.add(friendsOfCurrentUser[x])
    friends = set(friends)
    final = friendsOfFriends.difference(friends)
    return list(final)

def isEmailUnique(email):
    # use this to check if a email has already been registered
    conn, cursor = db.get_cursor()
    if cursor.execute("SELECT email FROM User WHERE email = '{0}'".format(email)):
        # this means there are greater than zero entries with that email
        cursor.close()
        conn.close()
        return False
    else:
        cursor.close()
        conn.close()
        return True

#Friend routes
@app.route("/friends", methods=['GET'])
@flask_login.login_required
def friend():
    uid1 = (flask_login.current_user.id)

    friends = friendTuple((flask_login.current_user.id))
    recs = friendRecs((flask_login.current_user.id))
    return render_template('friends.html', friends = friends, recs = recs)

@app.route('/friends', methods=['POST'])
def add_friend():
    if request.method == 'POST':
        friend = request.form.get('friends')
        uid1 = (flask_login.current_user.id)
        
        if isEmailUnique(friend) == True:
            return render_template('friends.html', msg = 'Email does not exist!', friends = friendTuple(flask_login.current_user.id))
        else:
             uid2 = getUserIdFromEmail(friend)

        if isFriendsWith(uid1, uid2):
            return render_template('friends.html', msg = 'You are already friends with that user', friends = friendTuple(flask_login.current_user.id))
        else:
            try:
                conn, cursor = db.get_cursor()
                cursor.execute("INSERT INTO Friends (id1, id2) VALUES (%s, %s)", (uid1, uid2))
                conn.commit()
                cursor.close()
                return render_template('friends.html', msg='Friend added!', friends = friendTuple(flask_login.current_user.id))
            except:
                return render_template('friends.html', msg = 'Can not friend yourself!', friends = friendTuple(flask_login.current_user.id))
    else:
        return render_template('friends.html')

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