from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import requests

from .. import db # means from __init__.py
from ..models import Owner, User, WineDetails, WineEntry
from .auth import auth
from .apis import apis

tabs = Blueprint('tabs', __name__)

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

