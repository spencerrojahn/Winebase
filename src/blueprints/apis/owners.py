from flask import Blueprint, jsonify
from flask_login import current_user

owners = Blueprint('owners', __name__)

@owners.route('/list', methods=['GET'])
def owners_list():
    owners = current_user.owners
    owners_list = []

    for owner in owners:
        owner_dict = {
            "id": owner.id,
            "name": owner.name,
            "initials": owner.initials,
            "color_num": owner.color_num
            # Add other attributes as needed
        }
        owners_list.append(owner_dict)

    print(owners_list)
    return jsonify(owners_list)
