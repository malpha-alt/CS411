import db
import lookup
import datetime
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import json
import os

maps_bp = Blueprint('maps_bp', __name__, template_folder='templates')

@maps_bp.route('/maps/<int:user_id>', methods=['GET'])
def map(user_id):
  conn, cursor = db.get_cursor()
  cursor.execute("SELECT search_data FROM UserSearches WHERE userID = %s", (user_id,))
  user_searches = cursor.fetchall()
      
  #Add database information to a list to send to map creation
  concert_list = []
  for search in user_searches:
    results = json.loads(search[0])
    concert_list.extend(results)
  cursor.close()
  conn.close()

  #Builds the api call
  mapCall = 'https://maps.googleapis.com/maps/api/js?key=' + os.getenv('GOOGLE_DEV_API') + '&callback=initMap' # type: ignore
  return render_template('googleMap.html', mapCall=mapCall, concertList=concert_list)