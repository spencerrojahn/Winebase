from flask import Blueprint, request, jsonify
from flask_login import current_user
from sqlalchemy.sql import func

from datetime import datetime

from ... import db # means from __init__.py
from ...models import Owner, User, WineDetails, WineEntry, Cellar

wines = Blueprint('wines', __name__)

OWNER_COLOR_MAP = {
    1: 'blue',
    2: 'red',
    3: 'green',
    4: 'orange',
    5: 'yellow'
}

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

    data_return_dict = dict()

    query = (
        db.session.query(*[
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
        ])
        .select_from(WineEntry)
        .join(WineDetails)
        .join(Owner)
        .outerjoin(Cellar, WineEntry.cellar_id == Cellar.id) # doesn't have to be associated to a table
        .filter(WineEntry.user_id == current_user.id)
    )

    # Count query (subquery)
    count_query = (
        db.session.query(
            func.count()
        )
        .select_from(WineEntry)
        .join(WineDetails)
        .join(Owner)
        .outerjoin(Cellar, WineEntry.cellar_id == Cellar.id)
        .filter(WineEntry.user_id == current_user.id)
    )

    if filters:
        print(filters)

        # handle undrank vs drank
        if filters['undrank'] and not filters['drank']:
            query = query.filter(WineEntry.drank == False)
            count_query = count_query.filter(WineEntry.drank == False)
        elif not filters['undrank'] and filters['drank']:
            query = query.filter(WineEntry.drank == True)
            count_query = count_query.filter(WineEntry.drank == True)

        # query = query.filter(WineDetails.varietals.ilike(f"%cabernet%"))
        # add them to both above queries





    total_count = count_query.scalar()
    print(total_count)
    data_return_dict['total_count']= total_count

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


    data_return_dict['response'] = query.all()

    return data_return_dict



@wines.route('/list', methods=['POST'])
def wine_list():

    # cellar = Cellar(name='HOME', height=18, width=9, depth=2, user=current_user)
    # cellar2 = Cellar(name='APT', height=3, width=6, depth=1, user=current_user)
    # db.session.add(cellar)
    # db.session.add(cellar2)
    # db.session.commit()

    # owner = Owner(name='Spencer', initials='SCKR', color_num=1, user=current_user)
    # owner1 = Owner(name='Dad', initials='DAD', color_num=2, user=current_user)
    # db.session.add(owner)
    # db.session.add(owner1)
    # db.session.commit()

    

    response_dict = dict()

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

    response_dict['totalCount'] = query_response['total_count']
    response_dict['response'] = [
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
        for entry in query_response['response']
    ]

    return jsonify(response_dict)


def create_wine_details(body):
    wine_details = WineDetails()
    wine_details.winery_name = body['wineryName']

    if body['wineryLocation'] != '':
        wine_details.winery_location = body['wineryLocation']

    if body['vineyardLocation'] != '':
        wine_details.vineyard_location = body['vineyardLocation']

    if body['wineName'] != '':
        wine_details.wine_name = body['wineName']

    wine_details.varietals = body['varietals']
    wine_details.vintage = int(body['vintage'])

    if body['expertRaterName'] != '':
        wine_details.expert_rater_name = body['expertRaterName']
        wine_details.expert_rating = int(body['expertRating'])

    if body['personalRating'] != '':
        wine_details.personal_rating = int(body['personalRating'])

    return wine_details


def edit_wine_details(body, wine_entry):
    wine_details = wine_entry.details

    if body['wineryName'] != wine_details.winery_name:
        wine_details.winery_name = body['wineryName']

    if body['wineryLocation'] != wine_details.winery_location:
        if body['wineryLocation'] == '':
            wine_details.winery_location = None
        else:
            wine_details.winery_location = body['wineryLocation']
    
    if body['vineyardLocation'] != wine_details.vineyard_location:
        if body['vineyardLocation'] == '':
            wine_details.vineyard_location = None
        else:
            wine_details.vineyard_location = body['vineyardLocation']
    
    if body['wineName'] != wine_details.wine_name:
        if body['wineName'] == '':
            wine_details.wine_name = None
        else:
            wine_details.wine_name = body['wineName']
    
    if body['varietals'] != wine_details.varietals:
        wine_details.varietals = body['varietals']
    
    if body['vintage'] != wine_details.vintage:
        wine_details.vintage = body['vintage']
    
    if body['expertRaterName'] != wine_details.expert_rater_name:
        if body['expertRaterName'] == '':
            wine_details.expert_rater_name = None
            wine_details.expert_rating = None
        else:
            wine_details.expert_rater_name = body['expertRaterName']
            wine_details.expert_rating = int(body['expertRating'])

    if body['personalRating'] != wine_details.personal_rating:
        if body['personalRating'] == '':
            wine_details.personal_rating = None
        else:
            wine_details.personal_rating = int(body['personalRating'])



def create_wine_entry(body, owner, wine_details):
    wine_entry = WineEntry()
    wine_entry.entry_date = datetime.strptime(body['entryDate'], "%Y-%m-%d")
    
    if body['drinkDate'] != '':
        wine_entry.drink_date = body['drinkDate']

    wine_entry.drank = True if body['drank'] == 'YES' else False

    if body['purchasePrice'] != '':
        wine_entry.purchase_price = float(body['purchasePrice'])

    if body['aquisitionInfo'] != '':
        wine_entry.acquisition_info = body['aquisitionInfo']

    if body['personalNotes'] != '':
        wine_entry.personal_notes = body['personalNotes']

    if body['cellar'] != '':

        cellar = Cellar.query.filter_by(name=body['cellar']).first()
        wine_entry.cellar = cellar

        # iterate through cellar wine entries and look for 
        # any wine entries that contain this same cellar location
        # and return to form if it exists

        cellar_wine_entries = cellar.wine_entries
        for wine_entry in cellar_wine_entries:
            if wine_entry.cellar_location == body['binLocation']:
                return None



        wine_entry.cellar_location = body['binLocation']

    
    wine_entry.user = current_user
    wine_entry.owner = owner
    wine_entry.details = wine_details

    return wine_entry



def edit_wine_entry(body, owner, wine_entry, wine_entry_id):

    current_owner = wine_entry.owner

    if (current_owner.initials != owner.initials):
        wine_entry.owner = owner

    if body['drinkDate'] != wine_entry.drink_date:
        if body['drinkDate'] == '':
            wine_entry.drink_date = None
        else:
            wine_entry.drink_date = body['drinkDate']

    wine_entry.drank = True if body['drank'] == 'YES' else False

    if body['purchasePrice'] != '':
        wine_entry.purchase_price = float(body['purchasePrice'])

    if body['aquisitionInfo'] != wine_entry.acquisition_info:
        if body['aquisitionInfo'] == '':
            wine_entry.acquisition_info = None
        else:
            wine_entry.acquisition_info = body['aquisitionInfo']

    if body['personalNotes'] != wine_entry.personal_notes:
        if body['personalNotes'] == '':
            wine_entry.personal_notes = None
        else:
            wine_entry.personal_notes = body['personalNotes']
    
    if wine_entry.cellar != None:
        if body['cellar'] != wine_entry.cellar.name:
            if body['cellar'] == '':
                wine_entry.cellar = None
            else:
                cellar = Cellar.query.filter_by(name=body['cellar']).first()
                wine_entry.cellar = cellar
    else:
        if body['cellar'] != '':
            cellar = Cellar.query.filter_by(name=body['cellar']).first()
            wine_entry.cellar = cellar
    

    if body['binLocation'] != wine_entry.cellar_location:
        if body['binLocation'] == '':
            wine_entry.cellar_location = None
        else:
            cellar_wine_entries = wine_entry.cellar.wine_entries
            for wine_entry in cellar_wine_entries:
                if wine_entry.id != wine_entry_id and wine_entry.cellar_location == body['binLocation']:
                    return False
            wine_entry.cellar_location = body['binLocation']

    return True



@wines.route('/add', methods=['POST'])
def wines_add():
    body = request.get_json()
    print(body)

    try:

        if body['owner'] == 'new-owner':
            # create new owner
            owner = Owner(
                        name=body['newOwnerName'], 
                        initials=body['newOwnerInitials'], 
                        color_num= int(body['newOwnerColor'])
                    )

            # check if this user already exists and then return to form if it does already
            db.session.add(owner)
        else:
            owner = Owner.query.filter_by(initials=body['owner']).first()


        wine_details = create_wine_details(body)
        db.session.add(wine_details)

        wine_entry = create_wine_entry(body, owner, wine_details)
        if wine_entry == None:
            # return bin location taken error
            return jsonify({"message": "Bin location taken"}), 500

        db.session.add(wine_entry)

        db.session.commit()

        # If successful, return a success JSON response
        return jsonify({"status": "success"}), 200

    except Exception as e:
        # If an exception occurs, return an error JSON response
        return jsonify({"status": "error", "error_message": str(e)})


@wines.route('/edit/<int:wine_entry_id>', methods=['POST'])
def wines_edit(wine_entry_id):
    body = request.get_json()
    # print(body)

    try:

        wine_entry = WineEntry.query.filter_by(id=wine_entry_id).first()

        if body['owner'] == 'new-owner':
            # create new owner
            owner = Owner(
                        name=body['newOwnerName'], 
                        initials=body['newOwnerInitials'], 
                        color_num= int(body['newOwnerColor'])
                    )

            # check if this user already exists and then return to form if it does already
            db.session.add(owner)
        else:
            owner = Owner.query.filter_by(initials=body['owner']).first()

        

        edit_wine_details(body, wine_entry)



        updated = edit_wine_entry(body, owner, wine_entry, wine_entry_id)

        if updated == False:
            # return bin location taken error
            return jsonify({"message": "Bin location taken"}), 500

        db.session.commit()

        # If successful, return a success JSON response
        return jsonify({"status": "success"}), 200

    except Exception as e:
        # If an exception occurs, return an error JSON response
        return jsonify({"status": "error", "error_message": str(e)})




# get singular wine
@wines.route('/get/<int:wine_entry_id>', methods=['GET'])
def wines_get(wine_entry_id):

    try:

        wine_entry = WineEntry.query.filter_by(id=wine_entry_id).first()
        print(wine_entry.cellar)

        cellar_name = None
        if wine_entry.cellar != None:
            cellar_name = wine_entry.cellar.name

        wine_entry_dict = {
            'cellar': cellar_name,
            'cellar_location': wine_entry.cellar_location,
            'owner': wine_entry.owner.initials,
            'vintage': wine_entry.details.vintage,
            'varietals': wine_entry.details.varietals,
            'wine_name': wine_entry.details.wine_name,
            'winery_name': wine_entry.details.winery_name,
            'winery_location': wine_entry.details.winery_location,
            'vineyard_location': wine_entry.details.vineyard_location,
            'entry_date': wine_entry.entry_date,
            'drank': wine_entry.drank,
            'drink_date': wine_entry.drink_date,
            'acquisition_info': wine_entry.acquisition_info,
            'personal_notes': wine_entry.personal_notes,
            'purchase_price': wine_entry.purchase_price,
            'expert_rater_name': wine_entry.details.expert_rater_name,
            'expert_rating': wine_entry.details.expert_rating,
            'personal_rating': wine_entry.details.personal_rating
        }

        return (jsonify(wine_entry_dict))

    except Exception as e:
        # If an exception occurs, return an error JSON response
        return jsonify({"status": "error", "error_message": str(e)})


# delete singular wine
@wines.route('/delete/<int:wine_entry_id>', methods=['DELETE'])
def wines_delete(wine_entry_id):

    try:
        
        # delete wine details by id after deleting wine entry (get id first obviously)
        wine_entry = WineEntry.query.get(wine_entry_id)
        wine_details_id = wine_entry.details_id
        db.session.delete(WineDetails.query.get(wine_details_id))
        db.session.delete(wine_entry)
        db.session.commit()

        # If successful, return a success JSON response
        return jsonify({"status": "success"})

    except Exception as e:
        # If an exception occurs, return an error JSON response
        return jsonify({"status": "error", "error_message": str(e)})


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