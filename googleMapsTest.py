from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import * # type: ignore
from wtforms.validators import DataRequired
from datetime import datetime
import os
import requests

googleMapsTest = Flask(__name__)
googleMapsTest.config['SECRET_KEY'] = os.urandom(32)

@googleMapsTest.route('/', methods=['GET', 'POST'])
def testApi():
    return render_template('googleMap.html')

@googleMapsTest.route('/search', methods=['GET', 'POST']) # type: ignore #Search page
def search():
    form = SearchForm()
    artist = request.form.get('query')
    date = request.form.get('date')
    
    results = []
    api_key = "KEY"
    headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
    }
    if artist and date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        date = date_object.strftime('%d-%m-%Y')
        query_params = {"artistName": artist, 
                        "date": date}  # Use the user input here
        endpoint = "https://api.setlist.fm/rest/1.0/search/setlists"
        response = requests.get(endpoint, params=query_params, headers=headers).json()
        if response.get("setlist"):
            for item in response.get("setlist"):
                artist_name = item.get("artist").get("name")
                concert_date = item.get("eventDate")
                city = item.get("venue").get("city").get("name")
                venue = item.get("venue").get("name")
                venue_coords = item.get("venue").get("city").get("coords")
                lat = venue_coords.get("lat")
                long = venue_coords.get("long")
                results.append({'artist': artist_name, 
                                'date': concert_date, 
                                'venue': venue,
                                'city': city,
                                'lat': lat,
                                'long': long})
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