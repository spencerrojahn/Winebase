from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db # means from __init__.py
from .models import User

tabs = Blueprint('tabs', __name__)
auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists.', category='error')
        elif len(username) < 2:
            flash('username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username, password_hash=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('tabs.wines'))

    return render_template('register.html', user=current_user)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_username = User.query.filter_by(username=username).first()
        if user_username:
            if check_password_hash(user_username.password_hash, password):
                flash('Logged in successfully with username!', category='success')
                login_user(user_username, remember=True)
                return redirect(url_for('tabs.wines'))
            else:
                # print('username - wrong password')
                flash('Invalid username or password', category='error')
        else:
            flash('Invalid username or password', category='error')
            # print('username does not exist')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/")
@auth.route("/wines")
@tabs.route("/wines")
@login_required
def wines():
    return render_template("tab-pages/wines.html", user=current_user, username=current_user.username, tab_name="WINES")

@auth.route("/cellars")
@tabs.route("/cellars")
@login_required
def cellars():
    return render_template("tab-pages/cellars.html", user=current_user, username=current_user.username, tab_name="CELLARS")

