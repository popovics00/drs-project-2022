from db_config import db
from marshmallow import Schema, fields
import json

from models.cryptocurrency import Cryptocurrency

class Usercrypto(db.Model):
    email = db.Column(db.String(100), nullable = False, primary_key = True)
    cryptocurrency = db.Column(db.String(100), nullable = False, primary_key = True)
    balance = db.Column(db.Float(), nullable = False)

    def __repr__(self):
        return '<Task %r' % self.id
    
    def to_json(self):
        return dict(email = self.email,
                    cryptocurrency = self.cryptocurrency,
                    balance = self.balance)
        
class UsercryptoSchema(Schema):
    email = fields.Str()
    cryptocurrency = fields.Str()
    balance = fields.Float()