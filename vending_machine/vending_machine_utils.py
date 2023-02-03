from .models import (VendingMachine, db)


def create_vending_machine(data):
    name, location = data.get('name'), data.get('location')
    new_vending_machine = VendingMachine(name=name, location=location)
    db.session.add(new_vending_machine)
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


def delete_vending_machine(data):
    id = data.get('id')
    vending_machine = VendingMachine.query.filter_by(id=id).first()
    if vending_machine is None:
        return {'status': 'Bad Request'}, 400
    db.session.delete(vending_machine)
    db.session.commit()
    return {'status': 'OK'}, 200
