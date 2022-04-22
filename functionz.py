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
        print(user + password)
        sql = f"SELECT * FROM users WHERE userid = '{user}' AND pass = '{password}'"
        print(sql)
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


# def query_order(orderid):
#     """ query parts from the parts table """
#     conn = None
#     try:
#         conn = psycopg2.connect(host = hostname,
#         dbname = database,
#         user= username,
#         password = pwd,
#         port = port_id)
#
#         cur = conn.cursor()
#
#         sql = f"SELECT * FROM users WHERE orderid = '{orderid}''"
#         cur.execute(sql, (orderid))
#         rows = cur.fetchall()
#         print("---The Requested Order Is---\n")
#         for row in rows:
#             print(row)
#         cur.close()
#         return rows
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
