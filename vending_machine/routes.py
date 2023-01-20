from flask import current_app as app
from flask import (request, jsonify)
from flask.helpers import make_response
from .models import (VendingMachine, db)

@app.route('/vending_machine')
def list_vending_machine():
    results = VendingMachine.query.all()
    return jsonify({"vending_machines":results})

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
    db.session.delete(vending_machine)
    db.session.commit()
    return jsonify({"status": "OK"})