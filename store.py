from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from functionz import update_product_price,delete_product
#login_attempt,query_order,insert_address,insert_order,insert_product
import psycopg2

app = Flask(__name__)

# Configurations for connecting to the database using sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/sweetshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database Information
# hostname = 'localhost'
# database = 'sweetshop'
# username = 'postgres'
# pwd = 'postgres'
# port_id = 5432

# conn is the connection object
# conn = psycopg2.connect(
#             host = hostname,
#             dbname = database,
#             user= username,
#             password = pwd,
#             port = port_id)

# Creating a cursor object so we can execute SELECT statemetns
# cur = conn.cursor()

# create_script = '''CREATE TABLE IF NOT EXISTS employee(
#                 id int PRIMARY KEY,
#                 name varchar(40) NOT NULL,
#                 salary int,
#                 dept_id varchar(30))'''

# insert_script = 'INSERT INTO employee (id,name,salary,dept_id) VALUES (%s,%s,%s,%s)'
# insert_value = (1,'James', 12000, 'D1')
# cur.execute(insert_script, insert_value)

# We use execute function to execute the actual scripts
# cur.execute(create_script)

# Commit function is need
# conn.commit()

# x = login_attempt("bond007","password")
# print(x)
#
# y = query_order(2)
# print(y)
#
# # Creating an SQLALCHEMY object
# db = SQLAlchemy(app)
#
# print()
# print()
# print()
# print()
#
# insert_address('Alop','Tampa','FL','31224')
#
# print()
# print()
# print()
# print()
#
# insert_order('jojo17',4,12,5,'Alop','Tampa')
#
# print()
# print()
# print()
# print()
#
# insert_product(42,1,'raq','pizza',421,'good')
#
# print()
# print()
# print()
# print()

update_product_price(1,324)

print()
print()
print()
print()

delete_product(2)
# Route decorator tells Flask what url to use to trigger a function
@app.route('/')
def index():
    # fetches all the records in the Favquotes table and stores them in the result variable
    # result = Favquotes.query.all()
    return render_template('index.html')


# These are endpoints
# What the applications will be responding with if they go to the
# /about or /quotes sections
@app.route('/about_us')
def quotes():
    return render_template('about_us.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/contact_us')
def contact():
    print(request.args)
    return render_template('contact_us.html')

@app.route('/login_signup')
def login():
    return render_template('login_signup.html')

@app.route('/prodicks')
def ma():
    return render_template('prodicks.html')

# A GET message is send, and the server returns data. POST. Used to send HTML form data to the server.
@app.route('/process', methods = ['POST'])
def process():
    author = request.form['fname']

    # redirects user to the homepage when form is submitted
    return redirect(url_for('index.html'))

# cur.close()
# conn.close()
