import datetime
import random
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from blueprints.transactionCrypto import StatusTransakcije
from models.cryptotransaction import Cryptotransaction
from models.user import User
from db_config import db
import json
from werkzeug.security import generate_password_hash, check_password_hash

user_stats = Blueprint('user_stats', __name__)

@user_stats.route('/load-profile')
def load_profile():
    id = request.args.get('id')
    if id:
        #ako id postoji izvrsi upit nad bazom
        existing_user = User.query.get(int(id))
        return jsonify(existing_user.as_dict())
    return jsonify({})

@user_stats.route('/update-profile', methods=['POST'])
def update_profile():
    id = request.form.get('userId')
    name = request.form['firstName']
    lastname = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    city = request.form['city']
    country = request.form['country']
    phoneNumber = request.form['phoneNum']
    
    user = User.query.get(id)
    
    if password == "": #ako pass nije dodat onda uzimamo onaj koji se vec nalazi u korisniku
        update_user = User(id = id, name=name, lastname=lastname, email = email, password = user.password, address = address, city = city,
                       country = country, phoneNumber = phoneNumber, balance=user.balance, verificated = user.verificated, 
                       cardNumber = user.cardNumber, expDate = user.expDate, securityCode = user.securityCode)
    else:
        update_user = User(id = id, name=name, lastname=lastname, email = email, password = generate_password_hash(password), address = address, city = city,
                       country = country, phoneNumber = phoneNumber, balance=user.balance, verificated = user.verificated, 
                       cardNumber = user.cardNumber, expDate = user.expDate, securityCode = user.securityCode)
    
    db.session.delete(user)
    db.session.commit() #jer je id primarni kljuc a na isti id zelimo da upisemo i novog korisnika pa prvo moramo da
    #sacuvamo brisanje kako bi se id oslobodio da na njega upisemo izmene
    db.session.add(update_user)
    db.session.commit()
    return jsonify(update_user.as_dict())

@user_stats.route('/verify-account', methods=["POST"])
def verify():
    id = request.form.get('userIdCard')
    card_num = request.form.get('cardNumber')
    exp_date = request.form.get('expDate')
    code = request.form.get('code')
    status = 0
    counter = 0
    
    user= User.query.get(id)
    #brisanje postojeceg, tj update
    
    idd = str(random.getrandbits(128))
    transaction = Cryptotransaction(receiverId = id, 
                              senderId = '/', 
                              cryptocurrency = '/', 
                              amount= 0, 
                              price = -1, 
                              total = -1, 
                              transactionId = idd, 
                              date = datetime.datetime.now(), 
                              status = StatusTransakcije.Rejected.value[0])
    
    if card_num != '4242-4242-4242-4242':
        status = 1
        counter += 1
    if exp_date == '02/23':
        status = 1
        counter += 1
    if code == '123':
        status = 1
        counter += 1
    
    if status == 1 and counter == 3:
         db.session.delete(user)
         db.session.commit()
         user_by_id = User(id = id, name=user.name, lastname=user.lastname, email = user.email, password = user.password, address = user.address, city = user.city,
                       country = user.country, phoneNumber = user.phoneNumber, balance=user.balance, verificated = True, 
                       cardNumber = card_num, expDate = exp_date, securityCode = code)
         db.session.add(user_by_id)
         db.session.commit()
         
         transaction.status = StatusTransakcije.Approved.value
         db.session.add(transaction)
         db.session.commit()
         return jsonify(user_by_id.as_dict())
    else:
        db.session.add(transaction)
        db.session.commit()
        return jsonify(user.as_dict())
