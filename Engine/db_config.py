from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from flask import Flask

db = SQLAlchemy()
DB_NAME = "database_drs"
mysql = MySQL()

app=Flask(__name__)
app.config['SECRET_KEY'] = 'ioahdoah oaihdoah'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'stefan'
app.config['MYSQL_DATABASE_DB'] = DB_NAME
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:stefan@localhost:3306/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql.init_app(app)
db.init_app(app) 