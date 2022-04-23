from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

hostname = 'localhost'
database = 'sweetshop'
username = 'postgres'
pwd = 'postgres'
port_id = 5432

def login_attempt(user, password):
    """ query parts from the parts table """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"SELECT * FROM users WHERE userid = '{user}' AND pass = '{password}'"
        cur.execute(sql, (user, password))

        # fetchall function gets all the records for the query
        # this will return a list of tuples like this [(0,1,2)], every set of () is an individual record
        rows = cur.fetchall()
        print("The number of users: ", cur.rowcount)
        count = cur.rowcount
        for row in rows:
            print(row)
        cur.close()
        return count #Count of 1 means the user input is a match in the DB, 0 means it's not.
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def query_order(orderid):
    """ query orders based on orderid
        We could also do this based off userid instead... might be better.
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()

        sql = f"SELECT * FROM orders WHERE orderid = {orderid}"
        cur.execute(sql)
        rows = cur.fetchall()
        print("---The Requested Order Is---\n")
        for row in rows:
            print(row)
        cur.close()
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_address(street, city, state, zipcode):
    """ Inserts address into DB, if it does not already exist.
        Check console to see the SQL statement sent.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, do nothing, we assume address exists if error.
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        print()
        sql = f"INSERT INTO addresses(street,city,state,zipcode) VALUES ('{street}','{city}','{state}','{zipcode}')"
        print("Insert address statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("Possible Address Already Exists")
        return False; #Exists, or worse...
    finally:
        if conn is not None:
            conn.close()

def insert_order(userid, productid, quantity, totalcost, street, city):
    """ Inserts order into DB.
        NOTE: address pk(street,city) has to be existent in DB. To get around this use insert_addresses() first.
        NOTE: No need to add orderid. The DB was made to use orderid as a serial number, so it iterates when new orders are added.
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, order-success.html(if we make one) or do nothing | IF FALSE: Error, give user something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"INSERT INTO orders(userid, productid, quantity, totalcost, street, city) VALUES ('{userid}',{productid},{quantity},{totalcost},'{street}','{city}')"
        print("Insert order statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()

def insert_product(productid, storeid, name, foodtype, price, description): #TO BE FINISHED
    """ Inserts product into DB.
        NOTE: storeid has to be existent in DB..
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, give something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"INSERT INTO products(productid, storeid, name, foodtype, price, description) VALUES ({productid},{storeid},'{name}','{foodtype}',{price},'{description}')"
        print("Insert product statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()


def update_product_price(productid, new_price):
    """ UPDATES product price in DB.
        NOTE: productid must be within the DB.
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, give something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"UPDATE products SET price = {new_price} WHERE productid = {productid}"
        print("Update product price statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()


def delete_product(productid): #TO BE FINISHED
    """ Deletes product from DB based on productid.
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, give something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"DELETE FROM products WHERE productid = {productid}"
        print("Delete product statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()
