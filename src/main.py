"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Task
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager, jwt_required
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'El_que_no_salta_es_paco'
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200
@app.route('/register', methods=['POST'])
def register():
        if request.method == 'POST':
            data = request.get_json()
            new_user = None
            new_user = User(
                username=data["username"],
                password=sha256.hash(data["password"]),
                mail=data["mail"],
                name = data["name"],
                lastname = data["lastname"],
                rut = data["rut"]
            )
            print(new_user.serialize())
            db.session.add(new_user)
            db.session.commit()
            if new_user:
                return jsonify({
                    "papu": "inserto"
                }), 200
            else:
                return jsonify(#{
                    #"status": "la wea se rompio"
                    data
                #}
                ), 400

@app.route('/login', methods= ['POST'])
def login():
    if request.method == 'POST':
        user = User()
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        if user is None:
            return jsonify({
            "error": "el usuario no existe"
        }), 404
        if sha256.verify(data["password"], user.password):

            mivariable = create_access_token(identity=data["username"])
            refresh = create_refresh_token(identity=data["username"])
            return jsonify({
                "token": mivariable,
                "refresh": refresh,
                "user": user.serialize()
                }), 200

        return jsonify({
            "error": "la contraseña no es valida"
            }), 400  
@jwt_required        
@app.route('/newtask', methods=['POST'])
def hand_new_task():
    if request.method == 'POST':
        data = request.get_json()
        new_task = Task(
            title=data["title"],
            date=data["date"],
            location=data["location"],
            description=data["description"],
            payment=data["payment"]
        )
        db.session.add(new_task)
        if new_task:
            db.session.commit()
            return jsonify({
                "tarea":"insertada"
            }), 200
        else:
            return jsonify({
                "tarea": "no insertada"
            }), 400
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
