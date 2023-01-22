import datetime
import random
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from blueprints.transactionCrypto import StatusTransakcije
from models.cryptotransaction import Cryptotransaction
from models.user import User
from db_config import db
import json

deposit = Blueprint('deposit', __name__)

@deposit.route("/deposit-money", methods=['POST'])
def deposit_money():
    id = request.form.get('id')
    money = request.form.get('money')
    
    user = User.query.get(id)
    user.balance += int(money)
    db.session.commit()
    
    idd = str(random.getrandbits(128))
    transaction = Cryptotransaction(receiverId = id, 
                              senderId = '/', 
                              cryptocurrency = '/', 
                              amount= 0, 
                              price = money, 
                              total = money, 
                              transactionId = idd, 
                              date = datetime.datetime.now(), 
                              status = StatusTransakcije.Approved.value)
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(user.balance)