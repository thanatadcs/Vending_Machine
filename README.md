# Vending_Machine
## Requirement
```
pip install flask
pip install flask-sqlalchemy
```
## Run
```
flask --app vending_machine run
```
## Check list
- [x] Should be able to manage (create edit delete) vending machine.
- [x] There is a stock for each vending machine
- [x] Api to add/edit/remove item from stock
- [x] Listing for vending machine stock products
- [x] Able to edit a specific field on its own for both vending machine and product
## APIs  (JSON format)

### Manage vending machine via ```/vending_machine```

GET: List all vending machines and each of their product.

POST: Create a new vending machine. (required ```name``` (string) and ```location``` (string) fields)

PUT: Update existing vending machine fields specify by ```id``` (interger) field. (required ```id``` field, other fields are optional).

DELETE: Delete existing vending machine specify by ```id``` (integer) field.

### Manage product via ```/product```

GET: List all products.

POST: Create a new product (required ```name``` (string), ```price``` (float), ```quantity``` (integer), and ```vending_machine_id``` (integer) fields and vending machine corresponding to ```vending_machine_id``` must exists)

PUT: Update existing product specify by ```id``` (integer) field. (required ```id``` field, other fields are optional).

DELETE: Delete existing product specify by ```id``` (interger) field.

**Note: Deleteing a vending machine will deletes all products associated with that vending machine.**\
**More note: POST, PUT, DELETE required JSON body for input data.**
