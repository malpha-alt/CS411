from flask import url_for, Blueprint, jsonify
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
    return jsonify(user_details)