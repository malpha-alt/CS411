from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import * # type: ignore
from wtforms.validators import DataRequired
from datetime import datetime
from dotenv import load_dotenv
import os
import requests


googleMapsTest = Flask(__name__)
googleMapsTest.config['SECRET_KEY'] = os.urandom(32)
load_dotenv() #Loads the .env file
api_key = os.getenv('SETLIST_API_KEY')
headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
}

concertList = []

@googleMapsTest.route('/storedata', methods=['POST']) #Appends the selected result to the list of concerts
def storedata():
    session['selectedResult'] = request.get_json()
    concertList.append(session.get('selectedResult', [])[0])
    return '', 200

@googleMapsTest.route('/', methods=['GET', 'POST'])
def testApi():
    mapCall = 'https://maps.googleapis.com/maps/api/js?key=' + os.getenv('GOOGLE_MAP_API') + '&callback=initMap'
    return render_template('googleMap.html', mapCall=mapCall, concertList=concertList)

@googleMapsTest.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    artist = request.form.get('query') # Result from search bar
    date = request.form.get('date') #Result from date

    results = []
    if artist and date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        date = date_object.strftime('%d-%m-%Y') #Formats form date into query param format
        query_params = {"artistName": artist, 
                        "date": date}  # Use the user input here
        endpoint = "https://api.setlist.fm/rest/1.0/search/setlists"
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