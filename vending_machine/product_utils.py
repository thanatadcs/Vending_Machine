from .models import VendingMachine, Product, db


def create_product(data):
    name, price, quantity, vm_id = (
        data.get("name"),
        data.get("price"),
        data.get("quantity"),
        data.get("vending_machine_id"),
    )
    if VendingMachine.query.get(vm_id) is None:
        return {"status": "Bad Request"}, 400
    new_product = Product(
        name=name, price=price, quantity=quantity, vending_machine_id=vm_id
    )
    db.session.add(new_product)
    db.session.commit()
    return {"status": "OK"}, 200


def update_product(data):
    id, name, price, quantity, vm_id = (
        data.get("id"),
        data.get("name"),
        data.get("price"),
        data.get("quantity"),
        data.get("vending_machine_id"),
    )
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return {"status": "Bad Request"}, 400
    if name is not None:
        product.name = name
    if price is not None:
        product.price = name
    if quantity is not None:
        product.quantity = name
    if vm_id is not None:
        product.vending_machine_id = name
    db.session.commit()
    return {"status": "OK"}, 200


def delete_product(data):
    id = data.get("id")
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return {"status": "Bad Request"}, 400
    db.session.delete(product)
    db.session.commit()
    return {"status": "OK"}, 200
