from flask import current_app as app
from flask import (request, jsonify)
from flask.helpers import make_response
from .models import (VendingMachine, Product, db)


# Vending machine
@app.route('/vending_machine')
def list_vending_machine():
    results = VendingMachine.query.all()
    return jsonify({"vending_machine": results})


@app.route('/vending_machine', methods=['POST', 'PUT'])
def create_vending_machine():
    if request.method not in ['POST', 'PUT']:
        return make_response(jsonify({'status': 'Bad Request'}), 400)

    data: dict = request.get_json()
    required_fields = {'name', 'location'} if request.method == 'POST' else {'id'}
    if not data or not (required_fields <= data.keys()):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    if request.method == 'POST':
        # Create vending machine
        name, location = data.get('name'), data.get('location')
        new_vending_machine = VendingMachine(name=name, location=location)
        db.session.add(new_vending_machine)
    elif request.method == 'PUT':
        # Update vending machine
        id, name, location = data.get('id'), data.get('name'), data.get('location')
        vending_machine = VendingMachine.query.filter_by(id=id).first()
        if name is not None: vending_machine.name = name
        if location is not None: vending_machine.location = name
        db.session.commit()
    return jsonify({"status": "OK"})


@app.route('/vending_machine', methods=['DELETE'])
def delete_vending_machine():
    data: dict = request.get_json()
    required_fields = set(['id'])
    if not data or not (required_fields <= data.keys()):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    id = data.get('id')
    vending_machine = VendingMachine.query.filter_by(id=id).first()
    if vending_machine is None:
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    db.session.delete(vending_machine)
    db.session.commit()
    return jsonify({"status": "OK"})


# Product
@app.route('/product')
def list_product():
    results = Product.query.all()
    return jsonify({"product": results})


@app.route('/product', methods=['POST'])
def create_product():
    data: dict = request.get_json()
    required_fields = set(['name', 'price', 'quantity', 'vending_machine_id'])
    if not data or not (required_fields <= data.keys()):
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
    if not data or not (required_fields <= data.keys()):
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
    if not data or not (required_fields <= data.keys()):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    id = data.get('id')
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return make_response(jsonify({'status': 'bad request'}), 400)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"status": "OK"})
