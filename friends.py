import db
import lookup
import datetime
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user

friends_bp = Blueprint('friends_bp', __name__, template_folder='templates')

def friendTuple(uid):
    friendIds = getUsersFriends(uid)
    friends = []
    for i in friendIds:
        friends.append((lookup.getFirstNameFromId(i[0]), lookup.getEmailFromId(i[0]), i[0]))
    return friends

def friendRecs(uid):
    friends = friendTuple(uid)
    #adds current user to friends list so the user isn't recommended to themself
    friends.append((lookup.getFirstNameFromId(uid), lookup.getEmailFromId(uid), uid))
    friendsOfFriends = set()
    for i in range(len(friends)):
        friendsOfCurrentUser = friendTuple(friends[i][2])
        for x in range(len(friendsOfCurrentUser)):
            friendsOfFriends.add(friendsOfCurrentUser[x])
    friends = set(friends)
    final = friendsOfFriends.difference(friends)
    return list(final)

def getUsersFriends(uid):
    conn, cursor = db.get_cursor()
    cursor.execute("SELECT id2 FROM Friends WHERE id1 = '{0}'".format(uid))
    return cursor.fetchall()

def isFriendsWith(uid, uid2):
    conn, cursor = db.get_cursor()
    print(uid)
    print(uid2)
    if cursor.execute("SELECT id2 FROM Friends WHERE id1 = '{0}' AND id2 = '{1}'".format(uid, uid2)):
        print(cursor.execute("SELECT id2 FROM Friends WHERE id1 = '{0}' AND id2 = '{1}'".format(uid, uid2)))
        return True
    else:
        return False


#Friend routes
@friends_bp.route("/friends", methods=['GET'])
@flask_login.login_required
def friend():
    uid1 = (flask_login.current_user.id)

    friends = friendTuple((flask_login.current_user.id))
    recs = friendRecs((flask_login.current_user.id))
    return render_template('friends.html', friends = friends, recs = recs)

@friends_bp.route('/friends', methods=['POST'])
def add_friend():
    if request.method == 'POST':
        friend = request.form.get('friends')
        uid1 = (flask_login.current_user.id)
        
        if lookup.isEmailUnique(friend) == True:
            return render_template('friends.html', msg = 'Email does not exist!', friends = friendTuple(flask_login.current_user.id))
        else:
             uid2 = lookup.getUserIdFromEmail(friend)

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

