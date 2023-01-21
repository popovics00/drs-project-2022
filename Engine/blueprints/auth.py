from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models.user import User
from db_config import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    user_logged_in = None
    email = request.form.get('email')
    password = request.form.get('password')
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
         if check_password_hash(existing_user.password, password):
             #korisnik postoji i uneta sifra je ista kao ona u bazi
             user_logged_in = existing_user.id
    return jsonify(user_logged_in)

@auth.route('/sign-up', methods=['POST'])
def sign_up():
   user_register = False 
    
   first_name = request.form.get('firstName')
   lastname = request.form.get('lastName')
   address = request.form.get('address')
   city = request.form.get('city')
   country = request.form.get('country')
   phoneNumber = request.form.get('phoneNum')
   email = request.form.get('email')
   password = request.form.get('password')
   
   existing_user = User.query.filter_by(email=email).first()
   if not(existing_user):
       new_user = User(name = first_name, lastname = lastname, address = address, city = city, country = country, phoneNumber = phoneNumber,
                   email = email, password = generate_password_hash(password, method='sha256'), balance = 0, verificated = False,
                   cardNumber = "", expDate = "", securityCode="")
       db.session.add(new_user)
       db.session.commit()
       user_register = True
       print("New user created!")
   return jsonify(user_register)

   