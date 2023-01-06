from flask import request, jsonify, Blueprint
from db_config import db
import random, datetime
from enum import Enum

from models.usercrypto import Usercrypto
from models.user import User
from models.cryptotransaction import Cryptotransaction

class TransactionState(Enum):
    PROCESSING = 0,
    REJECTED = 1,
    APPROVED = 2

transCrypto_bp = Blueprint('transferCrypto', __name__)


@transCrypto_bp.route('/buycrypto', methods=['POST'])
def buycrypto():
    balance = 0

    id = request.form['id']
    amount = request.form['amount']
    crypto = request.form['crypto']
    price = request.form['price']

    buyer = User.query.get(id)

    #transakcija
    id = str(random.getrandbits(128))
    transaction = Cryptotransaction(receiverEmail = buyer.email, 
                              senderEmail = '/', 
                              cryptocurrency = crypto, 
                              amount= amount, 
                              price = price, 
                              total = float(amount) * float(price), 
                              transactionId = id, date = datetime.datetime.now(), 
                              status = TransactionState.REJECTED.value[0])

    if(float(amount) * float(price) <= buyer.balance):
        cryptoAccounts = Usercrypto.query.all()
        exists = False

        for cryptoAccount in cryptoAccounts:
            if(cryptoAccount.email == buyer.email and cryptoAccount.cryptocurrency == crypto):
                cryptoAccount.balance += float(amount)
                db.session.add(cryptoAccount)
                db.session.commit()

                buyer.balance -= float(amount) * float(price)
                db.session.add(buyer)
                db.session.commit()

                exists = True

        if(exists == False):
            cryptoAccount = Usercrypto(email = buyer.email, cryptocurrency = crypto, balance = float(amount))
            try:
                db.session.add(cryptoAccount)
                db.session.commit()  
                
                buyer.balance -= float(amount) * float(price)
                db.session.add(buyer)
                db.session.commit()   
            except Exception as e:
                return jsonify(e), 400

        transaction.status = TransactionState.APPROVED.value
        db.session.add(transaction)
        db.session.commit()

        return jsonify("Your purchase was successful!"), 200
    else:
        db.session.add(transaction)
        db.session.commit()
        return jsonify('Insufficient funds'), 200