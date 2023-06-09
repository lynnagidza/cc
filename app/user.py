"""User blueprint"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    """Logic for user login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home'))

        flash(error)
    return render_template('user/login.html')

@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    """Logic for user registration"""
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                    (email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError as e:
                if 'email' in str(e):
                    error = f"User with email {email} is already registered."
                elif 'username' in str(e):
                    error = f"User {username} is already registered."
            else:
                return redirect(url_for("user.login"))

        flash(error)
    return render_template('user/register.html')

@user_bp.route('/logout')
def logout():
    """Logic for user logout"""
    session.clear()
    return render_template('main/home.html')

@user_bp.route('/profile')
def profile():
    """Logic to fetch and display the user's profile information"""
    return render_template('user/profile.html')

@user_bp.route('/order-history')
def order_history():
    """Logic to fetch and display the user's order history"""
    return render_template('user/order_history.html')

@user_bp.route('/track-order/<int:order_id>')
def track_order(order_id):
    """Logic to fetch and display the tracking information for a specific order"""
    return render_template('user/track_order.html', order_id=order_id)

@user_bp.route('/reset-password')
def reset_password():
    """Logic for password reset functionality"""
    return render_template('user/reset_password.html')

# Add more routes specific to the user blueprint
@user_bp.before_app_request
def load_logged_in_user():
    """Loads the logged in user"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

def login_required(view):
    """Decorator to ensure user is logged in before accessing a route"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view
# Error handlers

@user_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@user_bp.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
