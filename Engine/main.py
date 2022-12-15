from flask import Flask
from blueprints.auth import auth
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(port=5001, debug=True)