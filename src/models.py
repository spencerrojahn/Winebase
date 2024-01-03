from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # One-to-many relationship with WineEntry
    wine_entries = db.relationship('WineEntry', back_populates='user')


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    initials = db.Column(db.String(4), unique=True, nullable=False)
    color_num = db.Column(db.Integer, unique=True, nullable=False)

    # One-to-many relationship with WineEntry
    wine_entries = db.relationship('WineEntry', back_populates='owner')


class WineDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winery_name = db.Column(db.String(255), nullable=False)         # winery name (NOT optional)
    winery_location = db.Column(db.String(500), nullable=True)      # winery location (optional)
    vineyard_location = db.Column(db.String(500), nullable=True)    # vinary where the grapes were grown (optional)
    wine_name = db.Column(db.String(150), nullable=True)            # wine name (optional)
    varietals = db.Column(db.String(255), nullable=False)           # varietal(s) (NOT optional) - can be multiple
    vintage = db.Column(db.Integer, nullable=False)                 # vintage (NOT optional)
    expert_rater_name = db.Column(db.String(150), nullable=True)    # expert rater name (optional)
    expert_rating = db.Column(db.Integer, nullable=True)            # expert rating 100 point scale (optional)       
    personal_rating = db.Column(db.Integer, nullable=True)          # personal rating 1-5 (optional)

    # One-to-one relationship with WineEntry
    wine_entry = db.relationship('WineEntry', back_populates='details', uselist=False)


class WineEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)                    
    entry_date = db.Column(db.Date, nullable=False)
    drink_date = db.Column(db.Date, nullable=True)
    drank = db.Column(db.Boolean, nullable=False, default=False)
    cellar = db.Column(db.String(50), nullable=True)
    cellar_location = db.Column(db.String(10), nullable=True)
    purchase_price = db.Column(db.Float, nullable=True)
    entry_description = db.Column(db.String(1000), nullable=True)
    personal_notes = db.Column(db.String(1000), nullable=True)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='wine_entries')

    # Foreign key to Owner
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    owner = db.relationship('Owner', back_populates='wine_entries')

    # One-to-one relationship with WineDetails
    details_id = db.Column(db.Integer, db.ForeignKey('wine_details.id'), unique=True, nullable=False)
    details = db.relationship('WineDetails', back_populates='wine_entry')

