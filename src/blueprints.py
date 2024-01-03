from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from . import db # means from __init__.py
from .models import Owner, User, WineDetails, WineEntry

tabs = Blueprint('tabs', __name__)
auth = Blueprint('auth', __name__)
apis = Blueprint('apis', __name__)

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

@apis.route('/wines/<int:user_id>', methods=['GET'])
def get_wines(user_id):


    user = User.query.filter_by(id=user_id).first()
    entries = {}
    for entry in user.wine_entries:
        if entry.owner.initials in entries:
            entries[entry.owner.initials].append(entry.cellar_location)
        else:
            entries[entry.owner.initials] = [entry.cellar_location]
    return jsonify(entries)





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


    # EXAMPLE FOR HOW GET works with sending parameters

    # get_wines_api = url_for('apis.get_wines', user_id=current_user.id, _external=True)
    # response = requests.get(get_wines_api)

    # if response.status_code == 200:
    #     # Parse the JSON response
    #     json_data = response.json()
    #     print(json_data)
    # else:
    #     # Handle the case when the internal API returns an error
    #     print('Internal API error')
    
    return render_template("tab-pages/wines.html", user=current_user, username=current_user.username, tab_name="WINES")

@auth.route("/cellars")
@tabs.route("/cellars")
@login_required
def cellars():
    return render_template("tab-pages/cellars.html", user=current_user, username=current_user.username, tab_name="CELLARS")






# # user = User(username='john_doe')

#                 # Create a wine entry with details
#                 owner = Owner.query.filter_by(initials='SCKR').first()

#                 wine_details = WineDetails(
#                     winery_name='Chateau St. Jean',
#                     winery_location='Sonoma County, CA, US',                                        # optional
#                     # vineyard_location=', Sonoma Valley, Sonoma County',                     # optional
#                     # wine_name='Cinq Cepages',                                                       # optional
#                     varietals='Cabernet Franc', 
#                     vintage=2018,                                                                   # optional
#                     expert_rater_name='Robert Parker',                                              # optional
#                     expert_rating=91,                                                               # optional
#                     personal_rating=4                                                               # optional
#                 )

#                 wine_entry = WineEntry(
#                     entry_date='2023-04-01', 
#                     drink_date='2026-04-07',                # optional
#                     drank=False,                            # optional
#                     cellar='DAD',                           # optional
#                     cellar_location='F4-F',                 # optional
#                     purchase_price=55.5,                    # optional
#                     entry_description='Q4 Wine Shipment',   # optional
#                     # personal_notes='Bold and tanniny',       # optional
#                     user=user_username, 
#                     owner=owner,
#                     details = wine_details
#                 )

                

#                 # Save to the database
#                 # db.session.add(user)
#                 # db.session.add(owner)
#                 db.session.add(wine_entry)
#                 db.session.add(wine_details)
#                 db.session.commit()



    # # Query the user and their wine entries
    # queried_user = User.query.filter_by(username='john_doe').first()
    # print(f"User: {queried_user.username}")

    # for entry in queried_user.wine_entries:
    #     print(f"Wine Entry Date: {entry.entry_date}, Details: {entry.details.description}")




# sorted_entries = sorted(queried_user.wine_entries, key=lambda entry: entry.details.vintage or 0)


# # Filter wine entries by varietals containing "char"
#     filtered_entries = [entry for entry in queried_user.wine_entries if "char" in entry.details.varietals.lower()]

