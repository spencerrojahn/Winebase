from flask import Blueprint, render_template # redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
# import requests

from .. import db # means from __init__.py
# from ..models import Owner, User, WineDetails, WineEntry, Cellar
# from .auth import auth

base_bp = Blueprint('base', __name__)
tabs = Blueprint('tabs', __name__)

@base_bp.route("/")
@base_bp.route("/wines")
@tabs.route("/wines")
@login_required
def wines():

    # cellar = Cellar(name='HOME', height=18, width=9, depth=2)
    # owner = Owner(name='Spencer', initials='SCKR', color_num=1)
    # owner1 = Owner(name='Dad', initials='DAD', color_num=2)

    # owner = Owner.query.filter_by(initials='SCKR').first()
    # # # # # owner = Owner.query.filter_by(initials='DAD').first()

    # cellar = Cellar.query.filter_by(name='HOME').first()

    # wine_details = WineDetails(
    #     winery_name='Chalk Hill',
    #     winery_location='Russian River Valley, CA, US',                                        # optional
    #     vineyard_location='Chalk Hill Estate, Russian River Valley',                     # optional
    #     # wine_name='Reserve 8555 Red Blend',                                                       # optional
    #     varietals='Chardonnay', 
    #     vintage=2021,                                                                   # optional
    #     # expert_rater_name='Robert Parker',                                              # optional
    #     # expert_rating=97,                                                               # optional
    #     # personal_rating=5                                                               # optional
    # )

    # wine_entry = WineEntry(
    #     entry_date='2023-09-04', 
    #     drink_date='2024-05-20',                # optional
    #     # drank=True,                            # optional (False by default)
    #     purchase_price=46,                    # optional
    #     acquisition_info='Wine tasting purchase - 9/2/2023',   # optional
    #     # personal_notes='Bold and tanniny',       # optional
    #     user=current_user, 
    #     owner=owner,
    #     details = wine_details,
    #     cellar=cellar,                           # optional
    #     cellar_location='H5-F',                 # optional
    # )


    # db.session.add(cellar)
    # # # # # # Save to the database
    # # # # # # db.session.add(user)
    # db.session.add(owner)
    # db.session.add(owner1)
    # db.session.add(wine_entry)
    # db.session.add(wine_details)
    # db.session.commit()


    # delete wine details by id after deleting wine entry (get id first obviously)

    # wine_entry = WineEntry.query.get(2)
    # wine_details_id = wine_entry.details_id
    # db.session.delete(wine_entry)
    # db.session.delete(WineDetails.query.get(wine_details_id))
    # db.session.commit()

    # delete wine entry from cellar

    # wine_entry = WineEntry.query.get(2)
    # wine_entry.cellar = None
    # wine_entry.cellar_location = None
    # db.session.commit()

    # cellar = Cellar.query.get(1)
    # print(cellar.wine_entries)

    
    return render_template("tab-pages/wines.html", user=current_user, username=current_user.username, tab_name="WINES")

@base_bp.route("/cellars")
@tabs.route("/cellars")
@login_required
def cellars():
    return render_template("tab-pages/cellars.html", user=current_user, username=current_user.username, tab_name="CELLARS")


@base_bp.route("/owners")
@tabs.route("/owners")
@login_required
def owners():
    return render_template("tab-pages/owners.html", user=current_user, username=current_user.username, tab_name="OWNERS")

