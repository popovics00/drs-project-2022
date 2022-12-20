from flask import Flask
from blueprints.auth import auth
from blueprints.user_stats import user_stats
from blueprints.deposit import deposit
from flask_cors import CORS
from db_config import *

app.register_blueprint(auth)
app.register_blueprint(user_stats)
app.register_blueprint(deposit)

db.create_all(app=app)
CORS(app)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
    
