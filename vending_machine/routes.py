from flask import current_app as app
from flask import request, jsonify
from flask.helpers import make_response

from .models import Product, VendingMachine
from .vending_machine_utils import (
    create_vending_machine,
    update_vending_machine,
    delete_vending_machine,
)
from .product_utils import create_product, update_product, delete_product


def is_not_valid_field(actual_fields, required_fields):
    return not actual_fields or not (required_fields <= actual_fields.keys())


# Vending machine
@app.route("/vending_machine")
def list_vending_machine():
    results = VendingMachine.query.all()
    return jsonify({"vending_machine": results})


@app.route("/vending_machine", methods=["POST", "PUT", "DELETE"])
def modify_vending_machine():
    if request.method not in ["POST", "PUT", "DELETE"]:
        return make_response(jsonify({"status": "Bad Request"}), 400)

    required_fields_of_requests = {
        "POST": {"name", "location"},
        "PUT": {"id"},
        "DELETE": {"id"},
    }
    data: dict = request.get_json()
    required_fields = required_fields_of_requests[request.method]
    methods_to_vending_machine_functions_map = {
        "POST": create_vending_machine,
        "PUT": update_vending_machine,
        "DELETE": delete_vending_machine,
    }
    if is_not_valid_field(data, required_fields):
        status, status_code = {"status": "bad request"}, 400
    else:
        status, status_code = methods_to_vending_machine_functions_map[request.method]
    return make_response(jsonify(status), status_code)


# Product
@app.route("/product")
def list_product():
    results = Product.query.all()
    return jsonify({"product": results})


@app.route("/product", methods=["POST", "PUT", "DELETE"])
def modify_product():
    if request.method not in ["POST", "PUT", "DELETE"]:
        return make_response(jsonify({"status": "Bad Request"}), 400)

    required_fields_of_requests = {
        "POST": {"name", "price", "quantity", "vending_machine_id"},
        "PUT": {"id"},
        "DELETE": {"id"},
    }
    data: dict = request.get_json()
    required_fields = required_fields_of_requests[request.method]
    methods_to_product_functions_map = {
        "POST": create_product,
        "PUT": update_product,
        "DELETE": delete_product,
    }
    if is_not_valid_field(data, required_fields):
        status, status_code = {"status": "bad request"}, 400
    else:
        status, status_code = methods_to_product_functions_map[request.method]
    return make_response(jsonify(status), status_code)
