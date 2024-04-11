from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import * # type: ignore
from wtforms.validators import DataRequired
import requests
import os

googleMapsTest = Flask(__name__)
googleMapsTest.config['SECRET_KEY'] = os.urandom(32)


@googleMapsTest.route('/', methods=['GET', 'POST'])
def testApi():
    return render_template('googleMap.html')

@googleMapsTest.route('/search')
def search():
    form = SearchForm()
    return render_template('search.html', form=form)

class SearchForm(FlaskForm):
    ids = StringField("ID",validators=[DataRequired()])
    submit = SubmitField("Submit")
    csrf_token = HiddenField()

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>
    #                             
    googleMapsTest.run(host='0.0.0.0', port=5000, debug=True)