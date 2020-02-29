from app.lib import mysql
import json
import logging
from flask import jsonify, make_response, render_template, request


def index():
    sql = """SELECT name, id FROM `products`"""
    cnx, cursor = mysql.connect()
    cursor.execute(sql)
    results = cursor.fetchall()
    products = list()
    for result in results:
        print result
        products.append({"name": result[0], "id": result[1]})

    customer_id = request.cookies.get("customer_id")
    logging.debug("I got cookies %s" % request.cookies)
    sql = """SELECT first_name, last_name, id from `customers`"""
    cursor.execute(sql)
    results = cursor.fetchall()
    customers = list()
    current_customer = None
    for result in results:
        customer = {
            "first_name": result[0],
            "last_name": result[1],
            'id': result[2]
        }
        if customer_id and result[2] == int(customer_id):
            current_customer = customer
        customers.append(customer)

    if not current_customer:
        current_customer = customers[0]

    resp = make_response(render_template("index.html", products=products, customers=customers,
                                         current_customer=current_customer))

    return resp


# Populate the database with some data
def populate_database():
    # Create the tables
    cnx, cursor = mysql.connect()
    mysql.create_tables(cursor, cnx)

    # Fill the tables with something
    sql = """INSERT INTO `companies` (id, name) VALUES
            ('1', 'Onstine Corporation')"""
    cursor.execute(sql)

    sql = """INSERT INTO `customers` (id, first_name, last_name, company_id) VALUES
            ('1', 'Justin', 'Onstine', '1')"""
    cursor.execute(sql)

    sql = """INSERT INTO `customers` (id, first_name, last_name, company_id) VALUES
            ('2', 'Erin', 'Onstine', '1')"""
    cursor.execute(sql)

    sql = """INSERT INTO `products` (id, name, price) VALUES
            ('1', 'Apple', '2.00')"""
    cursor.execute(sql)

    sql = """INSERT INTO `products` (id, name, price) VALUES
            ('2', 'Toilet Paper', '2.25')"""
    cursor.execute(sql)

    sql = """INSERT INTO `products` (id, name, price) VALUES
            ('3', 'Pistachios', '7.00')"""
    cursor.execute(sql)
    cnx.commit()
    return jsonify({"message": "ok"}), 200


# A customer has added something to their shopping cart
def add_item_to_order():
    data = json.loads(request.data)
    customer_id = data.get("customer_id")
    product_id = data.get("product_id")
    quantity = int(data.get("quantity"))

    cnx, cursor = mysql.connect()
    sql = """SELECT quantity FROM `customer_orders` WHERE
             customer_id = {customer_id} and product_id = {product_id}""".format(customer_id=customer_id,
                                                                                 product_id=product_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    print results
    if results[0][0]:
        quantity += results[0][0]

    sql = """INSERT INTO `customer_orders` (customer_id, product_id, quantity) VALUES
             ('{customer_id}', '{product_id}', '{quantity}')
             ON CONFLICT(customer_id, product_id) DO UPDATE SET quantity={quan}""".format(customer_id=customer_id,
                                                                                          product_id=product_id,
                                                                                          quantity=quantity,
                                                                                          quan=quantity)
    try:
        cursor.execute(sql)
        cnx.commit()
    except:
        return jsonify({"message": "Ack!"}), 500
    return jsonify({"message": "ok"}), 200


# Get an updated total of the items in the shopping cart
def get_order_total():
    customer_id = request.args.get("customer_id")
    cnx, cursor = mysql.connect()
    sql = """SELECT products.name FROM `customer_orders` JOIN `products` ON customer_orders.product_id = products.id
    WHERE customer_id = {customer_id}""".format(customer_id=customer_id)
    cursor.execute(sql)

    sql = """SELECT sum(products.price * customer_orders.quantity) AS total FROM
             `customer_orders` JOIN `products` ON customer_orders.product_id = products.id WHERE
             customer_id = {customer_id}""".format(customer_id=customer_id)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        return jsonify({"message": "Ack!"}), 500
    return jsonify({"data": results[0]}), 200
