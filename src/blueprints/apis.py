from webbrowser import get
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from .. import db # means from __init__.py
from ..models import Owner, User, WineDetails, WineEntry, Cellar

apis = Blueprint('apis', __name__)

TABLE_COLUMNS = [
    WineEntry.id,
    Cellar.name,                    # cellar
    WineEntry.cellar_location,      # cellar location (bin)
    Owner.initials,                 # owner
    WineDetails.vintage,            # vintage
    WineDetails.varietals,          # varietals
    WineDetails.wine_name,          # wine name
    WineDetails.winery_name,        # winery name
    WineDetails.winery_location,    # winery location
    WineDetails.vineyard_location,  # vineyard location
    WineEntry.entry_date,           # entry date
    WineEntry.drink_date,           # drink date
    WineEntry.drank                 # drank (true or false)
]

TABLE_COLUMN_ID_TO_DB_VALUE = {
    'cellar-column-sort': [Cellar, 'name'],   
    'bin-location-column-sort': [WineEntry, 'cellar_location'],   
    'owner-column-sort': [Owner, 'initials'],   
    'vintage-column-sort': [WineDetails, 'vintage'],   
    'varietals-column-sort': [WineDetails, 'varietals'],  
    'wine-name-column-sort': [WineDetails, 'wine_name'],   
    'winery-name-column-sort': [WineDetails, 'winery_name'], 
    'winery-location-column-sort': [WineDetails, 'winery_location'],           
    'vineyard-location-column-sort': [WineDetails, 'vineyard_location'], 
    'entry-date-column-sort': [WineEntry, 'entry_date'],  
    'drink-date-column-sort': [WineEntry, 'drink_date'],   
    'drank-column-sort': [WineEntry, 'drank'] 
}


def add_cell(data):
    return data if data != None else '--'

def clean_up_date(date):
    if date is None:
        return '--'
    return date.strftime("%m/%d/%Y")

def wines_list_query(sortColumnId, sortOrder, filters, offset, limit):

    query = (
        db.session.query(*TABLE_COLUMNS)
        .select_from(WineEntry)
        .join(WineDetails)
        .join(Owner)
        .outerjoin(Cellar, WineEntry.cellar_id == Cellar.id) # doesn't have to be associated to a table
        .filter(WineEntry.user_id == current_user.id)
    )

    if filters:
        pass    # handle later 

        # query = query.filter(WineDetails.varietals.ilike(f"%cabernet%"))

        

    if sortColumnId:

        order_by_table = TABLE_COLUMN_ID_TO_DB_VALUE[sortColumnId][0]
        order_by_column_name = TABLE_COLUMN_ID_TO_DB_VALUE[sortColumnId][1]
            
        if not sortOrder:   # this will be true for asc and false for desc
             query = query.order_by(
                getattr(order_by_table, order_by_column_name).is_(None),
                getattr(order_by_table, order_by_column_name).desc()
            )
        else:
            query = query.order_by(
                getattr(order_by_table, order_by_column_name).is_(None),
                getattr(order_by_table, order_by_column_name)
            )
    

        
    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit) 

    return query.all()




@apis.route('/wines', methods=['POST'])
def get_wines():

    # Get the JSON payload from the request
    body = request.get_json()

    sortColumnId = body['sort']['value'] 
    sortOrder = body['sort']['order'] 

    filters = body['filters']
    offset = body['offset']
    limit = body['limit']


    query_response = wines_list_query(
        sortColumnId, 
        sortOrder, 
        filters, 
        offset, 
        limit
    )

    table_date = [
        [
            entry.id,
            add_cell(entry.name),   # this is cellar name (just functionality)
            add_cell(entry.cellar_location),
            entry.initials,
            add_cell(entry.vintage),
            entry.varietals,
            add_cell(entry.wine_name),
            entry.winery_name,
            add_cell(entry.winery_location),
            add_cell(entry.vineyard_location),
            clean_up_date(entry.entry_date),
            clean_up_date(entry.drink_date),
            entry.drank
        ]  
        for entry in query_response
    ]

    return jsonify(table_date)




# @apis.route('/validate_wine_form', methods=['POST'])
# def validate_wine_form():




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



# owner = Owner.query.filter_by(initials='SCKR').first()

#     wine_details = WineDetails(
#         winery_name='Roth Estate',
#         winery_location='Sonoma County, CA, US',                                        # optional
#         vineyard_location=', Sonoma Valley, Sonoma County',                     # optional
#         wine_name='Ode to the Beast',                                                       # optional
#         varietals='Cabernet Sauvignon', 
#         vintage=2015,                                                                   # optional
#         expert_rater_name='Robert Parker',                                              # optional
#         expert_rating=97,                                                               # optional
#         personal_rating=5                                                               # optional
#     )

#     wine_entry = WineEntry(
#         entry_date='2023-04-01', 
#         drink_date='2023-12-07',                # optional
#         drank=True,                            # optional
#         # cellar='DAD',                           # optional
#         # cellar_location='F4-F',                 # optional
#         purchase_price=120,                    # optional
#         entry_description='Q2 Wine Shipment',   # optional
#         # personal_notes='Bold and tanniny',       # optional
#         user=current_user, 
#         owner=owner,
#         details = wine_details
#     )



#     # Save to the database
#     # db.session.add(user)
#     # db.session.add(owner)
#     db.session.add(wine_entry)
#     db.session.add(wine_details)
#     db.session.commit()