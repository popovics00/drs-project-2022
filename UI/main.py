from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/user-stats')
def user_stats():
    return render_template('user_stats.html')

@app.route('/exchange')
def exchange():
    return render_template('exchangeCrypto.html')

if __name__ == "__main__":
    app.run(debug=True)