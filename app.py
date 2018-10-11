import os

from flask import Flask, flash, request, render_template, redirect, url_for, jsonify, g, session
from flaskext.mysql import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

""" Create an instance of the app"""
app = Flask(__name__)

""" MySQL connection & configurations """
"""	hiding configuration in environment variables"""
##########################################

# Loads a user if logged in. If not, displays website in an anonymous user view
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        cursor.execute("SELECT * FROM account WHERE account_id = %s", (user_id))
        userRow = cursor.fetchone()
        g.account = userRow
        g.user = userRow[1]		# Note: userRow[1] refers to the username column in the account table.
        						# 		Not sure how to NOT hardcode this. userRow['username'] doesn't work.

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Create a new message """
    if request.method == 'POST':
        someMessage = request.form['message']
        cursor.execute("INSERT INTO message(author_id, msg, author) VALUES (%s, %s, %s)", (session.get('user_id'), someMessage, g.user))
        connect.commit()

    """ Get all the rows from message table """
    cursor.execute("SELECT * FROM message")
    data = cursor.fetchall()

    """ Loop through & display messages through Jinja template """
    return render_template('messages.html', theMessages = data, aUser = g.user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Registers a new user. Validates that the username is not already taken.
    Hashes the password for security. """
    someUser = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check for existing user before registering
        cursor.execute("SELECT username FROM account WHERE username=%s", (username))
        user = cursor.fetchone()
        someUser = user

        if user is not None:
            return "User {0} is already registered.".format(username)
        else:
            # If the username isn't taken, register the user and hash the password
            cursor.execute("INSERT INTO account(username, password) VALUES (%s, %s)",
                (username, generate_password_hash(password),)
            )
            connect.commit()
            return "User successfully registered."
            # return redirect(url_for('auth.login'))

    #return render_template('auth/register.html', aUser=someUser, title='Register')
    return render_template('register.html', aUser = g.user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Log in a registered user by adding the user id to the session. """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM account WHERE username=%s", (username))
        user = cursor.fetchone()

        if user is None:
            return "A user with that username does not exist."
        elif not check_password_hash(user[2], password):    # this is hardcoded; don't know how to access row tuple by column name
            return "Incorrect password."
        else:
            session.clear()
            session['logged_in'] = True
            session['user_id'] = user[0]     # also hardcoded -- user[1] is referring to user_ID column of user table
            return redirect(url_for('index'))

    return render_template('login.html', aUser = g.user)

@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('create.html', aUser = g.user)

def get_msg(id):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """

    # This creates a new table with columns msg_id, author_id, and msg
    cursor.execute("SELECT msg_id, author_id, msg FROM message INNER JOIN account ON author_id = account_id WHERE msg_id=%s", (id,))
    message = cursor.fetchone()
    
    if message is None:
    	abort(404, "Post id {0} doesn't exist.".format(id))

    # If the author_id != account_id
    if message[1] != g.account[0]:
    	abort(403)

    return message

@app.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
	"""Update a message if the current user is the author."""

	# Get the msg_id
	message = get_msg(id)

	if request.method == 'POST':
		someMessage = request.form['message']
		cursor.execute("UPDATE message SET msg = %s WHERE msg_id = %s", (someMessage, id))
		connect.commit()
		return redirect(url_for('index'))

	return render_template('update.html', aUser = g.user, message = message)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_msg(id)
    cursor.execute("DELETE FROM message WHERE msg_id = %s", (id,))
    connect.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()