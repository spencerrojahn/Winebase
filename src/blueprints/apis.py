from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from .. import db # means from __init__.py
from ..models import Owner, User, WineDetails, WineEntry

def add_cell(data):
    return data if data != None else '--'

def clean_up_date(date):
    if date is None:
        return '--'
    
    return date.strftime("%m/%d/%Y")

apis = Blueprint('apis', __name__)

@apis.route('/wines/<string:username>', methods=['GET'])
def get_wines(username):

    user = User.query.filter_by(username=username).first()

    table_columns = [
        WineEntry.cellar,               # cellar
        WineEntry.cellar_location,      # cellar location (bin)
        Owner.initials,                 # owner
        WineDetails.vintage,            # vintage
        WineDetails.varietals,          # varietals
        WineDetails.wine_name,          # wine name
        WineDetails.winery_name,        # winery name
        WineDetails.winery_location,    # winery location
        WineDetails.vineyard_location,  # vineyard location
        WineEntry.entry_date,           # entry date
        WineEntry.drink_date            # drink date
    ]

    response_entries = (
        db.session.query(*table_columns)
        .join(Owner)
        .join(WineDetails)
        .filter(WineEntry.user_id == user.id)
        # .filter(WineDetails.varietals.ilike(f"%Cabernet%"))
        .order_by(WineEntry.drink_date) # .order_by(WineEntry.drink_date.desc())
        # .offset(25)  # Skip the first 25 entries (offset)
        .limit(25)
        .all()
    )

    table_date = [
        [
            add_cell(entry.cellar),
            add_cell(entry.cellar_location),
            entry.initials,
            add_cell(entry.vintage),
            entry.varietals,
            add_cell(entry.wine_name),
            entry.winery_name,
            add_cell(entry.winery_location),
            add_cell(entry.vineyard_location),
            clean_up_date(entry.entry_date),
            clean_up_date(entry.drink_date)
        ]  
        for entry in response_entries
    ]

    return jsonify(table_date)







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

