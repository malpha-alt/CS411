from flask import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


@app.route('/', methods=['GET', 'POST'])
def testApi():
    form = SearchForm()
    '''if form.validate_on_submit():
        name = form.ids.data  # Retrieve user input'''

    api_key = "wTfSxrRhdui7T5-UixKi2Kx6882zePogIG6D"
    headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
    }

    query_params = {"artistName": "The Beatles",
                    "city": "Boston",
                    "date": "18-08-1966"}  # Use the user input here
    
    requestName = query_params['artistName']
    requestCity = query_params['city']
    requestDate = query_params['date']

    endpoint = "https://api.setlist.fm/rest/1.0/search/setlists"
    response = requests.get(endpoint, params=query_params, headers=headers).json()
 
    artistSearch_text = ""
    for item in response.get("setlist"):
        if item.get("artist").get("name") == requestName and \
            item.get("venue").get("city").get("name") == requestCity and \
            item.get("eventDate") == requestDate:
            artist_name = item.get("artist").get("name")
        else:
            return("Invalid Parameters")
        
        setlist = ""
        for song_set in item.get("sets").get("set"):
            for song in song_set.get("song"):
                setlist += song.get("name") + "\n"

    artistSearch_text += 'Artist Name: ' + artist_name + '<br>' + '\n' + setlist
        
    return render_template('map.html', artistSearch_text=artistSearch_text)

class SearchForm(FlaskForm):
    ids = StringField("ID",validators=[DataRequired()])
    submit = SubmitField("Submit")
    csrf_token = HiddenField()

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>
    #
    app.run(host='0.0.0.0', port=5000, debug=True)