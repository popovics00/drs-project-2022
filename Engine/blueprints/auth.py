from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    print("USAO U LOGIN")
    return "ASASASASA"

@auth.route('/sign-up', methods=['POST'])
def sign_up():
   name = request.form.get('name')
   print(name)
   return jsonify(True)