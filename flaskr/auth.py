import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

# Create the authentication blueprint, responsible for authenticating users.
# This blueprint will need to be registered with the app.
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register new users to the blog app by grabbing the username and password
    from the form.
    """
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db() # grab the database from the global context.
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            result = db.execute(
                "SELECT id FROM user WHERE username = ?",
                (username,)
            ).fetchone()

            if result is not None:
                error = 'User {} is already registered'.format(username)

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        # If all else fails, show the user what went wrong.
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Takes the username and password from the login request, checks the password
    and logs the user in.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # results if successful is a dictionary:
        # {
        #   'id': id,
        #   'username': username,
        #   'password': hashed password,
        # }
        user = db.execute(
            "SELECT * FROM user WHERE username = ?",
            (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            # store the user id in the session so that we can access it in
            # other views.
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    """
    Before we make a user log in over and over again, we can check to see if
    that users' id is in the session, thereby skipping everything
    """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    """
    Requiring login for other views. We create a decorator for views that require
    login. Usage is:
    
    @login_required
    @bp.route(...)
    def some_view(stuff)
        ...
        render_template(view)
    """
    
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # When a user is logged in, their id is mapped to the global session.
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
        
