from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
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
                       nameOnCard = user.nameOnCard, cardNumber = user.cardNumber, expDate = user.expDate)
    else:
        update_user = User(id = id, name=name, lastname=lastname, email = email, password = generate_password_hash(password), address = address, city = city,
                       country = country, phoneNumber = phoneNumber, balance=user.balance, verificated = user.verificated, 
                       nameOnCard = user.nameOnCard, cardNumber = user.cardNumber, expDate = user.expDate)
    
    db.session.delete(user)
    db.session.commit() #jer je id primarni kljuc a na isti id zelimo da upisemo i novog korisnika pa prvo moramo da
    #sacuvamo brisanje kako bi se id oslobodio da na njega upisemo izmene
    db.session.add(update_user)
    db.session.commit()
    return jsonify(update_user.as_dict())

@user_stats.route('/verify-account', methods=["POST"])
def verify():
    id = request.form.get('userIdCard')
    user = request.form.get('user')
    card_num = request.form.get('cardNumber')
    exp_date = request.form.get('expDate')
    code = request.form.get('code')
    
    user_by_id = User.query.get(id)
    user_by_id.verificated = True
    user_by_id.nameOnCard = user
    user_by_id.cardNumber = card_num
    user_by_id.expDate = exp_date
    db.session.commit()
    return jsonify(user_by_id.as_dict())
