from flask import Blueprint, jsonify
from flask_login import current_user

cellars = Blueprint('cellars', __name__)

@cellars.route('/list', methods=['GET'])
def cellars_list():
    cellars = current_user.cellars
    cellars_list = []

    for cellar in cellars:
        cellar_dict = {
            "id": cellar.id,
            "name": cellar.name,
            "height": cellar.height,
            "width": cellar.width,
            "depth": cellar.depth,
            # Add other attributes as needed
        }
        cellars_list.append(cellar_dict)

    print(cellars_list)
    return jsonify(cellars_list)
