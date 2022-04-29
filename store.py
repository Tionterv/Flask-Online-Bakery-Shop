from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# from functionz import insert_user
from functionz import *

# from functionz import top_users,delete_product,update_product_price,login_attempt,query_order,insert_address,insert_order,insert_product,
# top_stores,product_price, query_products
import psycopg2

app = Flask(__name__)

# Configurations for connecting to the database using sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/sweetshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

store_id = 0
login_user = ""
flag = -1
signup = 0

@app.route('/process_login', methods =['POST'])
def process_login():
    # flag = -1
    username = request.form.get('userid')
    assword = request.form.get('password')
    global flag
    flag = login_attempt(username, assword)

    if flag == 1:
        global login_user
        login_user = username

    return render_template("login.html", flag=flag, username=username)

@app.route('/process_signup', methods =['POST'])
def process_signup():
    # flag = -1
    username = request.form.get('userid')
    name = request.form.get('name')
    email= request.form.get('email')
    assword = request.form.get('password')
    succ = insert_user(username, name, assword, email)

    global login_user 
    login_user = username

    global signup
    signup = 1

    global flag
    flag = -1
    if succ:
        flag = 1
    
    return render_template("signup.html", flag=flag, login_user=login_user)

# Route decorator tells Flask what url to use to trigger a function
@app.route('/')
def index():
    # fetches all the records in the Favquotes table and stores them in the result variable
    # result = Favquotes.query.all()
    return render_template('doodoobase.html', flag=flag, login_user=login_user)


@app.route('/store_find',methods=['POST','GET'])
def store_find():
    global store_id
    stoopidstore =int(request.form.get('storeid'))
    
    if stoopidstore != 0:
        store_id = stoopidstore

    if stoopidstore == 0:
        product_list = query_products(store_id)
    product_list = query_products(stoopidstore)
    return render_template('productss.html',product_list=product_list, stoopidstore=stoopidstore, login_user=login_user, flag=flag)

@app.route('/add-products', methods=['POST'])
def addTingzToCart():
    global nameParam
    # userid = request.form.get('userid')
    productid = int(request.form.get('productid'))
    quantity = int(request.form.get('quantitty'))
    totalcost = float(request.form.get('price_item'))
    store_info = query_store(store_id)

    print("\nDOODOO " + str(store_info) + "\n")

    street = store_info[store_id-1][2]
    city = store_info[store_id-1][3]
    insert_order(login_user, productid, quantity, totalcost, street, city) 

    return render_template('doodoobase.html', login_user=login_user, flag=flag)
    # return render_template("productss.html",storeid=storeid)

@app.route('/delete-products' , methods=['GET', 'POST'])
def removeTingsFromCart():
    orderid = int(request.form.get('orderid'))
    delete_order(orderid)
    return redirect("/cart")
    # return render_template("http://127.0.0.1:5000/cart")
# delete_product(2)

# These are endpoints
# What the applications will be responding with if they go to the
# /about or /quotes sections
@app.route('/about_us')
def quotes():
    return render_template('about_us.html', login_user=login_user, flag=flag)

@app.route('/cart')
def cart():
    prod_dembow = query_prods(login_user)
    # print(cart_items)
    # prod_names = query_prod_name(userid)
    return render_template('cart.html', prod_dembow=prod_dembow, login_user=login_user, flag=flag, signup=signup)

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html', login_user=login_user, flag=flag)

@app.route('/productss', methods=['GET', 'POST'])
def ma():
    return render_template('productss.html', login_user=login_user,flag=flag)

@app.route('/product')
def product():
    return render_template('product_page.html', login_user=login_user, flag=flag)

@app.route('/success')
def success():
    return render_template('success.html', login_user=login_user, flag=flag)

@app.route('/login')
def login():
    return render_template('login.html', login_user=login_user, flag=flag)  

@app.route('/checkout', methods=['POST','GET'])
def process_checkout():
    prod_dembow = query_prods(login_user)

    payment_dembow = query_payment(login_user)
    total_cost = get_total(login_user)
    
    #make new page that says checkout is successful
    return render_template('checkout.html', prod_dembow=prod_dembow, payment_dembow=payment_dembow, total_cost=total_cost, login_user=login_user, flag=flag, signup=signup)  

@app.route('/error')
def error():
    return render_template('sumting_wrong.html')




# cur.close()
# conn.close()
