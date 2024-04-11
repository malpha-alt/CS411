from flask import Flask, render_template
from flask_wtf import * # type: ignore
from wtforms import * # type: ignore
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

    api_key = "KEY"
    headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
    }
    query_params = {"artistName": "The Beatles"}  # Use the user input here
    endpoint = "https://api.setlist.fm/rest/1.0/search/artists"
    response = requests.get(endpoint, params=query_params, headers=headers).json()
    artistSearch_text = ""
    iter = 1
    for item in response.get("artist"):
        artist_name = item.get("name")
        artistSearch_text += str(iter) +'. Artist Name: ' + artist_name + '<br>'
        iter += 1
    return render_template('map.html')

class SearchForm(FlaskForm):
    ids = StringField("ID",validators=[DataRequired()])
    submit = SubmitField("Submit")
    csrf_token = HiddenField()

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>
    #                             
    app.run(host='0.0.0.0', port=5000, debug=True)