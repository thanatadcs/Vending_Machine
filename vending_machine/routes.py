from flask import current_app as app
from flask import (request, jsonify)
from flask.helpers import make_response
from .models import (VendingMachine, Product, db)
from vending_machine_utils import *


def is_not_valid_field(actual_fields, required_fields):
    return not actual_fields or not (required_fields <= actual_fields.keys())


# Vending machine
@app.route('/vending_machine')
def list_vending_machine():
    results = VendingMachine.query.all()
    return jsonify({"vending_machine": results})


@app.route('/vending_machine', methods=['POST', 'PUT', 'DELETE'])
def modify_vending_machine():
    if request.method not in ['POST', 'PUT', 'DELETE']:
        return make_response(jsonify({'status': 'Bad Request'}), 400)

    required_fields_of_requests = {'POST': {'name', 'location'}, 'PUT': {'id'}, 'DELETE': {'id'}}
    data: dict = request.get_json()
    required_fields = required_fields_of_requests[request.method]
    if is_not_valid_field(data, required_fields):
        status, status_code = {'status': 'bad request'}, 400
    elif request.method == 'POST':  # Create vending machine
        status, status_code = create_vending_machine(data)
    elif request.method == 'PUT':  # Update vending machine
        status, status_code = update_vending_machine(data)
    elif request.method == 'DELETE':  # Delete vending machine
        status, status_code = delete_vending_machine(data)
    return make_response(jsonify(status), status_code)


# Product
@app.route('/product')
def list_product():
    results = Product.query.all()
    return jsonify({"product": results})


@app.route('/product', methods=['POST'])
def create_product():
    data: dict = request.get_json()
    required_fields = {'name', 'price', 'quantity', 'vending_machine_id'}
    if is_not_valid_field(data, required_fields):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    name, price, quantity, vm_id = \
        data.get('name'), data.get('price'), data.get('quantity'), data.get('vending_machine_id')
    if VendingMachine.query.get(vm_id) is None:
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    new_product = Product(name=name, price=price, quantity=quantity, vending_machine_id=vm_id)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"status": "OK"})


@app.route('/product', methods=['PUT'])
def update_product():
    data: dict = request.get_json()
    required_fields = set(['id'])
    if is_not_valid_field(data, required_fields):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    id, name, price, quantity, vm_id = \
        data.get('id'), data.get('name'), data.get('price'), data.get('quantity'), data.get('vending_machine_id')
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return make_response(jsonify({'status': 'bad request'}), 400)
    if name is not None: product.name = name
    if price is not None: product.price = name
    if quantity is not None: product.quantity = name
    if vm_id is not None: product.vending_machine_id = name
    db.session.commit()
    return jsonify({"status": "OK"})


@app.route('/product', methods=['DELETE'])
def delete_product():
    data: dict = request.get_json()
    required_fields = set(['id'])
    if is_not_valid_field(data, required_fields):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    id = data.get('id')
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return make_response(jsonify({'status': 'bad request'}), 400)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"status": "OK"})
