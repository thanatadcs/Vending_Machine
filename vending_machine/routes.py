from flask import current_app as app
from flask import (request, jsonify)
from flask.helpers import make_response
from .models import (VendingMachine, Product, db)

# Vending machine
@app.route('/vending_machine')
def list_vending_machine():
    results = VendingMachine.query.all()
    return jsonify({"vending_machine":results})

@app.route('/vending_machine', methods=['POST'])
def create_vending_machine():
    data: dict = request.get_json()
    required_fields = set(['name', 'location'])
    if not data or not (required_fields <= data.keys()):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    name, location = data.get('name'), data.get('location')
    new_vending_machine = VendingMachine(name=name, location=location)
    db.session.add(new_vending_machine)
    db.session.commit()
    return jsonify({"status": "OK"})

@app.route('/vending_machine', methods=['PUT'])
def update_vending_machine():
    data: dict = request.get_json()
    required_fields = set(['id', 'name', 'location'])
    if not data or not (required_fields <= data.keys()):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    id, name, location = data.get('id'), data.get('name'), data.get('location')
    vending_machine = VendingMachine.query.filter_by(id=id).first()
    vending_machine.name = name
    vending_machine.location = location
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
    return jsonify({"product":results})

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
    required_fields = set(['id', 'name', 'price', 'quantity', 'vending_machine_id'])
    if not data or not (required_fields <= data.keys()):
        return make_response(jsonify({'status': 'Bad Request'}), 400)
    id, name, price, quantity, vm_id = \
        data.get('id'), data.get('name'), data.get('price'), data.get('quantity'), data.get('vending_machine_id')
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return make_response(jsonify({'status': 'bad request'}), 400)
    product.name, product.price, product.quantity, product.vending_machine_id \
        = name, price, quantity, vm_id
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