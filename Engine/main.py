from flask import Flask
from blueprints.auth import auth
from blueprints.user_stats import user_stats
from blueprints.deposit import deposit
from blueprints.getCrypto import getCrypto_bp
from blueprints.transactionCrypto import transactionCrypto_bp
from blueprints.getTransactions import getTransactions_bp
from flask_cors import CORS
from db_config import *

app.register_blueprint(auth)
app.register_blueprint(user_stats)
app.register_blueprint(deposit)
app.register_blueprint(getCrypto_bp)
app.register_blueprint(transactionCrypto_bp)
app.register_blueprint(getTransactions_bp)

db.create_all(app=app)
CORS(app)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
    
