from flask import Flask
from blueprints.auth import auth
from flask_cors import CORS
from db_config import *

app.register_blueprint(auth)

db.create_all(app=app)
CORS(app)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
    
