from db_config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    lastname = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(50), nullable = False)
    city = db.Column(db.String(20), nullable = False)
    country = db.Column(db.String(20), nullable = False)
    phoneNumber = db.Column(db.String(10), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(150), nullable = False)
    balance = db.Column(db.Integer, nullable = False)
    verificated = db.Column(db.Boolean, nullable = False)
    securityCode = db.Column(db.String(4), nullable = False)
    cardNumber = db.Column(db.String(20), nullable = False)
    expDate = db.Column(db.String(6), nullable = False)
    
    def as_dict(self):
        return dict(id = self.id, name = self.name, lastname = self.lastname, address = self.address, city = self.city, country = self.country, 
                    phoneNumber = self.phoneNumber, email = self.email, balance = self.balance, securityCode = self.securityCode,
                    verificated = self.verificated, cardNumber = self.cardNumber, expDate = self.expDate)