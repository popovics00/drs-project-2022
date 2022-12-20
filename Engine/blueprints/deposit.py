from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
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
    
    return jsonify(user.balance)