from flask import current_app as app
from flask import (request, jsonify)
from flask.helpers import make_response
from .models import (VendingMachine, Product, db)


def check_required_fields(actual_fields, required_fields):
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
    if check_required_fields(data, required_fields):
        status, status_code = {'status': 'bad request'}, 400
    elif request.method == 'POST':  # Create vending machine
        status, status_code = create_vending_machine(data)
    elif request.method == 'PUT':  # Update vending machine
        status, status_code = update_vending_machine(data)
    elif request.method == 'DELETE':  # Delete vending machine
        status, status_code = delete_vending_machine(data)
    return make_response(jsonify(status), status_code)


def delete_vending_machine(data):
    id = data.get('id')
    vending_machine = VendingMachine.query.filter_by(id=id).first()
    if vending_machine is None:
        return {'status': 'Bad Request'}, 400
    db.session.delete(vending_machine)
    db.session.commit()
    return {'status': 'OK'}, 200


def update_vending_machine(data):
    id, name, location = data.get('id'), data.get('name'), data.get('location')
    vending_machine = VendingMachine.query.filter_by(id=id).first()
    if vending_machine is None:
        return {'status': 'Bad Request'}, 400
    if name is not None: vending_machine.name = name
    if location is not None: vending_machine.location = name
    db.session.commit()
    return {'status': 'OK'}, 200


def create_vending_machine(data):
    name, location = data.get('name'), data.get('location')
    new_vending_machine = VendingMachine(name=name, location=location)
    db.session.add(new_vending_machine)
    return {'status': 'OK'}, 200


# Product
@app.route('/product')
def list_product():
    results = Product.query.all()
    return jsonify({"product": results})


@app.route('/product', methods=['POST'])
def create_product():
    data: dict = request.get_json()
    required_fields = set(['name', 'price', 'quantity', 'vending_machine_id'])
    if check_required_fields(data, required_fields):
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
    if check_required_fields(data, required_fields):
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
    if check_required_fields(data, required_fields):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    id = data.get('id')
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return make_response(jsonify({'status': 'bad request'}), 400)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"status": "OK"})
