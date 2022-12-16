from db_config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    lastname = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(50), nullable = False)
    city = db.Column(db.String(20), nullable = False)
    country = db.Column(db.String(20), nullable = False)
    phoneNumber = db.Column(db.String(10), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(150), nullable = False)
    balance = db.Column(db.Integer, nullable = False)
    verificated = db.Column(db.Boolean, nullable = False)
    nameOnCard = db.Column(db.String(40), nullable = False)
    cardNumber = db.Column(db.String(20), nullable = False)
    expDate = db.Column(db.String(6), nullable = False)