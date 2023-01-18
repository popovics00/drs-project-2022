from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from flask import Flask
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
DB_NAME = "database_drs"
mysql = MySQL()
ma = Marshmallow()

app=Flask(__name__)
app.config['SECRET_KEY'] = 'ioahdoah oaihdoah'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Slatkamalasladakja123!'
app.config['MYSQL_DATABASE_DB'] = DB_NAME
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:Slatkamalasladakja123!@mysql/{DB_NAME}'

mysql.init_app(app)
db = SQLAlchemy(app)
db.init_app(app)
ma.init_app(app) 
