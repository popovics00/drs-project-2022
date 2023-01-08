from db_config import db
from marshmallow import Schema, fields
import json

from models.cryptocurrency import Cryptocurrency

class Cryptotransaction(db.Model):
    receiverId = db.Column(db.String(100), nullable = False, primary_key = True)
    senderId = db.Column(db.String(100), nullable = False)
    cryptocurrency = db.Column(db.String(100), nullable = False, primary_key = True)
    amount = db.Column(db.Float(), nullable = False)
    price = db.Column(db.Float(), nullable=False)
    total = db.Column(db.Float(), nullable= False)
    transactionId = db.Column(db.String(100), nullable = False, primary_key = True)
    date = db.Column(db.DateTime(), nullable = False)
    status = db.Column(db.Integer, nullable = False)  

    def __repr__(self):
        return '<Task %r' % self.id
    
    def to_json(self):
      return dict(receiverId = self.receiverId,
                  senderId = self.senderId,
                  cryptocurrency = self.cryptocurrency,
                  amount = self.amount,
                  price = self.price,
                  total = self.total,
                  transactionId = self.transactionId,
                  date = self.date,
                  status = self.status)