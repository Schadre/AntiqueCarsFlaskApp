from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import Car, db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

#Everything is connected by User_ID even if names aren't listed, the useer ID links the Antique cars to the owner
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'Test: {current_user_token.token}')

    car = Car(first_name, last_name, make, model, year, address, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


#Update End point
@api.route('cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.name = request.json['name']
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.address = request.json['address']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete Endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)