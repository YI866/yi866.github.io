import os
import base64
from typing import Union
import hashlib
import datetime
from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, create_refresh_token, \
    get_jwt_identity, get_current_user, jwt_required, JWTManager

app = Flask(__name__)
db: Flask = SQLAlchemy()
jwt = JWTManager()

# SECRET_KEY = base64.b64encode(os.urandom(256)).decode('ascii')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jwt_run.db"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = 'pYs98mYklp20V9sUq/iBd/bCsCTQ22HPsfraHwSBo8ZO/sBurSd5sIr/erH8GomofJ2fAYllw8C3zIDFZLKsCQ=='
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=3)

db.init_app(app)
jwt.init_app(app)


class User(db.Model):
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)

    @classmethod
    def init(cls):
        password = hashlib.md5('admin123'.encode('utf-8')).hexdigest()
        user = cls(username='admin', password=password)
        db.session.add(user)
        db.session.commit()


with app.app_context():
    if not db.engine.has_table('user'):
        db.create_all()
        User.init()


@jwt.user_lookup_loader
def user_loader_callback(jwt_header: dict, jwt_data: dict):
    return db.session.execute(db.select(User).filter_by(id=jwt_data['sub'])).one()[0]


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    password_encrypt = hashlib.md5(password.encode('utf-8')).hexdigest()
    user = db.session.execute(db.select(User).filter_by(username=username)).one()
    if not user:
        return jsonify(), 401
    user = user[0]
    if password_encrypt != user.password:
        return jsonify(), 401
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/user", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    ...
    return jsonify(log_user_id=current_user_id), 200


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_jwt():
    user_id = get_jwt_identity()
    return jsonify(access_token=create_access_token(identity=user_id, fresh=datetime.timedelta(minutes=1)))


@app.route("/user_fresh", methods=["GET"])
@jwt_required(fresh=True)
def protected_fresh():
    current_user = get_current_user()
    return jsonify(logged_in_as=current_user.username), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5030)
