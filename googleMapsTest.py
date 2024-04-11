from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import * # type: ignore
from wtforms.validators import DataRequired
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
    search_query = request.form.get('query')
    results = []

    api_key = "KEY"
    headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
    }
    if search_query:
        query_params = {"artistName": search_query}  # Use the user input here
        endpoint = "https://api.setlist.fm/rest/1.0/search/artists"
        response = requests.get(endpoint, params=query_params, headers=headers).json()
        iter = 1
        for item in response.get("artist"):
            artist_name = item.get("name")
            results.append({'title': artist_name})
    return render_template('search.html', form=form, results=results)

class SearchForm(FlaskForm):
    ids = StringField("ID",validators=[DataRequired()])
    submit = SubmitField("Submit")
    csrf_token = HiddenField()

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>
    #                             
    googleMapsTest.run(host='0.0.0.0', port=5000, debug=True)