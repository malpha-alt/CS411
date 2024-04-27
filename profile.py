import db
import lookup
import datetime
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user, login_required

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    default_profile_pic = url_for('static', filename='default-profile.png')
    profile_picture = current_user.profile_pic if current_user.profile_pic else default_profile_pic
    
    user_details = {
       'name': current_user.name,
       'email': current_user.email,
       'profile_picture': profile_picture
    }
    return render_template('profile.html', user=user_details)