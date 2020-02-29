from app.models import models
import logging
import sqlite3

DB_NAME = "orders"


def connect():
    cnx = sqlite3.connect("database.db")
    return cnx, cnx.cursor()


def create_tables(cursor, connection):
    for table in models.create_tables():
        logging.debug("Creating table %s" % table["name"])
        logging.debug(table["sql"])
        cursor.execute(table["sql"])
    connection.commit()
