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
            if(cryptoAccount.userId == buyer.id and cryptoAccount.cryptocurrency == crypto):
                cryptoAccount.balance += float(amount)
                db.session.add(cryptoAccount)
                db.session.commit()

                buyer.balance -= float(amount) * float(price)
                db.session.add(buyer)
                db.session.commit()

                exists = True

        if(exists == False):
            cryptoAccount = Usercrypto(userId = buyer.id, cryptocurrency = crypto, balance = float(amount))
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


@transCrypto_bp.route('/confirmConversion', methods=['POST'])
def confirmConversion():
    id = request.form["id"]
    myCrypto = request.form["myCrypto"]
    allCryptos = request.form["allCryptos"]
    inputConvertAmount = request.form["inputConvertAmount"]
    cryptoValue = request.form["cryptoValue"]
    myCryptoValue = request.form["myCryptoValue"]

    allUsersCryptos = Usercrypto.query.all()
    allMyCryptos = []
    exist = False
    for c in allUsersCryptos:
        if(c.userId == id):
            allMyCryptos.append(c)
            if(c.cryptocurrency == myCrypto):
                chosenMyCrypto = c
            if(c.cryptocurrency == allCryptos):
                chosenAnyCrypto = c
                exist = True

    if(chosenMyCrypto.balance < float(inputConvertAmount)):
        return jsonify('Amount is too high! You have ' + chosenMyCrypto.balance + ' ' + myCrypto + '.')
    
    myCryptoUsd = float(inputConvertAmount) * float(myCryptoValue)
    newCryptoAmount = myCryptoUsd / float(cryptoValue)

    chosenMyCrypto.balance -= float(inputConvertAmount)
    if(chosenMyCrypto.balance == 0):
        db.session.delete(chosenMyCrypto)
        db.session.commit()
    else:
        db.session.add(chosenMyCrypto)
        db.session.commit()
    
    if(exist):
        chosenAnyCrypto.balance += newCryptoAmount
        db.session.add(chosenAnyCrypto)
        db.session.commit()
    else:
        newCrypto = Usercrypto(userId = id, cryptocurrency = allCryptos, balance = float(newCryptoAmount))
        try:
            db.session.add(newCrypto)
            db.session.commit()
        except Exception as e:
            return jsonify(e), 400

    return jsonify("Convert succeded")