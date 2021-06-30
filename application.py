import os
#import requests
from datetime import datetime
from flask import Flask, session, request, jsonify, redirect, render_template, url_for, escape
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgresql://hqarjmdepnhngt:878b24ec455373807866474ef4b0bcac6f9dd1248e163a61f8ac77bd14c8d556@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d2mjumqpqcetd3")
db = scoped_session(sessionmaker(bind=engine))

# KEY for GOODREADER API
KEY = 'bTiJInyentTCuRDkQJ82gA'

# Login KEY!
app.secret_key = b'\xaf\xab\x95\xcc\xa8V\xa7\x02EK$3\xfdp\xa6\xc9'


#-------------------------------- START OF Index Route (Search PAGE) --------------------------------------

# Index aka Search Page!
@app.route("/", methods=['GET', 'POST'])
def index():

    #coming from index search
    if request.method == 'GET':

        if 'user_id' not in session:
            return redirect(url_for('login'))

        #the half phrase search including the full
        piz = db.execute("SELECT * FROM menu").fetchall()
        top = db.execute("SELECT * FROM topping").fetchall()

        #piz = db.execute("SELECT * FROM employee").fetchall()
        #top = db.execute("SELECT * FROM product").fetchall()
        print(piz)
        print(top)
        #if not exited return error
        if piz is None:
            return render_template("error.html", message="Something Went Wrong!")
        if top is None:
            return render_template("error.html", message="Something Went Wrong!")

        #if does return the files
        return render_template ("index.html", piz=piz, top=top)

    #showing user_name as they have to login to search
    "Logged is as %s" % escape(session['user_id'])

    # if user come through GET without login then redirectly to login
    #return render_template("index.html")
    piz = request.form.get("pizza")
    top = request.form.get("topping")
    size = request.form.get("size")
    str = piz + ';' + top + ';' + size

    # return to Add to Cart page!
    return redirect(url_for('AddToCart', str = str))


#-------------------------------- END OF INDEX (SEARCH PAGE) --------------------------------------


#-------------------------------- START OF AddToCart Route (AddToCart PAGE) --------------------------------------

# Logout Route Basic
@app.route('/addtocart', methods=['GET', 'POST'])
def AddToCart():

    data = (request.args['str']).split(';')
    piz = data[0]
    top = data[1]
    size = data[2]

    print("========================------------------------------")
    print(data)
    print("========================------------------------------")

    # Getting Ids:
    t_menu_code = db.execute("SELECT menu_code FROM menu WHERE menu_name = :menu_name",
                    {"menu_name" :piz}).fetchall()
    t_top_id = db.execute("SELECT top_id FROM topping WHERE top_name = :top_name",
                    {"top_name" :top}).fetchall()

    menu_code = t_menu_code[0][0]
    top_id = t_top_id[0][0]
    size = "p_" + size


    # Getting the Price:
    price = db.execute("SELECT "+ size +" FROM Price WHERE menu_code = :menu_code and top_id = :top_id",
                {"menu_code" :menu_code, "top_id" :top_id}).fetchall()

    print(str(piz) + " : " + str(menu_code))
    print(str(top) + " : " + str(top_id))
    print(str(size) + " : " + str(price))

    #piz = db.execute("SELECT * FROM employee").fetchall()
    #top = db.execute("SELECT * FROM product").fetchall()
    print("========================------------------------------")
    print(price)
    print("========================------------------------------")
    #if not exited return error
    if piz is None:
        return render_template("error.html", message="Something Went Wrong!")

    # POST transfering the details from FORM!
    if request.method == 'GET':
        return render_template("addtocart.html", message=price[0][0])
    else:

        # Getting Last Order Id:
        temp = db.execute("SELECT order_id FROM Orders order by order_id DESC limit 1").fetchall()

        # Coverting DateTime:
        t_ord_time = datetime.now()
        ord_time = t_ord_time.strftime("%Y-%m-%d %H:%M:%S")


        # Checking if the User Already A Customer:
        cus_id = db.execute("SELECT cus_id FROM Customer WHERE cus_name = :user_id", {"user_id" :session['user_id']}).fetchall()
        # if db.execute ("SELECT * FROM admin WHERE user_id = :user_id AND password =:password",
        #                 {"user_id": ch_user_id, "password": ch_password}).rowcount==0:
        cus_id = cus_id[0][0]

        # Incase User Not a Customer:
        if not cus_id:

            # Get Last User Id:
            p_cus_id = db.execute("SELECT cus_id FROM Customer ORDER BY cus_id DESC LIMIT 1").fetchall()
            # Creating New Id:
            cus_id = int(p_cus_id[0][0])+ 1
            cus_name = session['user_id'][0][0]

            # Inserting New Customer Data:
            db.execute("INSERT INTO customer (cus_id, cus_name) VALUES (:cus_id, :cus_name)",
                    {"cus_id": cus_id, "cus_name": cus_name})
            db.commit()

        # Inserting into the database Orders Table:
        db.execute("INSERT INTO orders (order_id, cus_id, ord_time) VALUES (:order_id, :cus_id, :ord_time)",
                {"order_id": int(temp[0][0]) + 1, "cus_id": cus_id, "ord_time" : ord_time})

        #finally committing the session (closing the session)
        db.commit()
        # Inserting into the database order_details Table:
        db.execute("INSERT INTO order_details (order_id, menu_code, top_id, price) VALUES (:order_id, :menu_code, :top_id, :price)",
                {"order_id": int(temp[0][0]) + 1, "menu_code": menu_code, "top_id" :top_id, "price" :price[0][0]})

        #finally committing the session (closing the session)
        db.commit()

        return render_template("addtocart.html", message="Order Placed! :)")


#-------------------------------- END OF AddToCart (AddToCart PAGE) --------------------------------------

#-------------------------------- START OF ADMIN (Admin PAGE) --------------------------------------

#app for route sending people from search page to books details page
@app.route("/admin", methods=['GET', 'POST'])
def admin():

    # POST transfering the details from FORM!
    if request.method == 'POST':

        # Check if the Admin Login:
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))

        data = request.form.get("get_data")

        # -- Most Valuable Customer --
        if data == 'value_customer':
            temp = db.execute("SELECT cus_id, count(order_id) as ords FROM Orders Group by cus_id").fetchall()
            print("---------------------")
            print(temp)
            print("---------------------")
            # Displaying the Result:
            return render_template('admin_result.html', msg=temp, query_title='Valuable Customer')

        # -- Highest Order Range --
        if data == 'high_value_order':
            temp = db.execute("SELECT ord_details.menu_code, ord_details.top_id, sum(ord_details.price) as high_value_order FROM Orders as ord "
                            	"INNER JOIN Order_details as ord_details " +
                            	"on ord.order_id = ord_details.order_id " +
                                "group by ord_details.menu_code, ord_details.top_id " +
                            	"Order by sum(ord_details.price) DESC LIMIT 5").fetchall()
            # Displaying the Result:
            return render_template('high_value_order.html', msg=temp, query_title='Highest Order Range')

        # -- Monthly Sales --
        if data == 'monthly_sales':
            temp = db.execute("SELECT TO_CHAR(ord.ord_time, 'Month') as month, sum(ord_details.price) as sales " +
                                "FROM Order_details as ord_details " +
            	                "INNER JOIN Orders as ord " +
                                "on ord_details.order_id = ord.order_id " +
                                "group by TO_CHAR(ord.ord_time, 'Month') " +
                                "order by sales DESC").fetchall()
            # Displaying the Result:
            return render_template('monthly_sales.html', msg=temp, query_title='Monthly Sales')

        # -- Net Profit --
        if data == 'net_profit':
            temp = db.execute("SELECT sup.menu_code, sup.top_id, (pt.p_small - sup.p_small) as small, "+
                                    "(pt.p_large - sup.p_large) as large " +
                                    "FROM Supplier as sup INNER JOIN Price as pt "
                                    "ON (sup.menu_code = pt.menu_code) and (sup.top_id = pt.top_id)").fetchall()
            # Displaying the Result:
            return render_template('net_profit.html', msg=temp, query_title='Net Profit')

        # -- Most Sold Pizza --
        if data == 'most_sold_pizza':
            temp = db.execute("SELECT mn.menu_name, count(ord_details.menu_code) as count_menu FROM Menu as mn "
                                "INNER JOIN Order_details as ord_details "
                                "on mn.menu_code = ord_details.menu_code "
                                "group by mn.menu_code").fetchall()
            # Displaying the Result:
            return render_template('most_sold_pizza.html', msg=temp, query_title='Most Sold Pizza')

        # -- Most Use Topping --
        if data == 'most_use_topping':
            temp = db.execute("SELECT tp.top_name, count(ord_details.top_id) as count_top FROM Topping as tp "
            	                "INNER JOIN Order_details as ord_details "
                                "on tp.top_id = ord_details.top_id "
                                "group by tp.top_name").fetchall()
            # Displaying the Result:
            return render_template('most_use_topping.html', msg=temp, query_title='Most Use Topping')

        # -- Count Valuable Supplier --
        if data == 'valuable_suppliers':
            temp = db.execute("SELECT sup_name, count(sup.menu_code) as menu_sold FROM Supplier as sup "
                                "INNER JOIN order_details as ord_details "
                                "on (sup.menu_code = ord_details.menu_code) and (sup.top_id = ord_details.top_id) "
                                "group by sup.sup_name").fetchall()
            # Displaying the Result:
            return render_template('valuable_suppliers.html', msg=temp, query_title='Valuable Suppliers')

        # -- Lifetime Order --
        if data == 'lifetime_order':
            temp = db.execute("SELECT order_id as total_orders FROM Orders " +
                                "where order_id in (SELECT count(order_id) " +
                                "FROM orders)").fetchall()
            # Displaying the Result:
            return render_template('lifetime_order.html', msg=temp[0][0], query_title='Lifetime Order')

        # If review already exited!
        return render_template("error.html", message="Something Went Wrong We are Working!")

    # GET render template with all variables plugin
    return  render_template("admin.html")

#-------------------------------- END OF Search Detials (Book Details Page) --------------------------------------

#-------------------------------- START OF Login Route (LOGIN PAGE) --------------------------------------

#for login and pass if the user available
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    # If user already login redirect to index (search page)
    if 'admin_id' in session:
        return redirect(url_for('admin'))

    # If user come via GET
    if request.method == 'GET':
        return render_template ("login.html")

    # If user come via POST render the form
    # transfering variables from FORM
    ch_user_id = request.form.get('user_id')
    ch_password = request.form.get('password')

    # Checking database for exact match for Username and Password! If not Return Error!
    if db.execute ("SELECT * FROM admin WHERE user_id = :user_id AND password =:password",
            {"user_id": ch_user_id, "password": ch_password}).rowcount==0:
        return render_template("error.html", message="Wrong Username or Password!")

    # If found transfering to session for later user_id
    session['admin_id'] = ch_user_id

    # return to Index page!
    return redirect(url_for('admin'))

#-------------------------------- END OF Login Route (Login Page) --------------------------------------

#-------------------------------- START OF Login Route (LOGIN PAGE) --------------------------------------

#for login and pass if the user available
@app.route("/login", methods=["GET", "POST"])
def login():

    # If user already login redirect to index (search page)
    if 'user_id' in session:
        return redirect(url_for('index'))

    # If user come via GET
    if request.method == 'GET':
        return render_template ("login.html")

    # If user come via POST render the form
    # transfering variables from FORM
    ch_user_id = request.form.get('user_id')
    ch_password = request.form.get('password')

    # Checking database for exact match for Username and Password! If not Return Error!
    if db.execute ("SELECT * FROM register WHERE user_id = :user_id AND password =:password",
            {"user_id": ch_user_id, "password": ch_password}).rowcount==0:
        return render_template("error.html", message="Wrong Username or Password!")

    # If found transfering to session for later user_id
    session['user_id'] = ch_user_id

    # return to Index page!
    return redirect(url_for('index'))

#-------------------------------- END OF Login Route (Login Page) --------------------------------------


#-------------------------------- START OF Register Route (REGISTRATION PAGE) --------------------------------------

#for registeration & adding to the data-base
@app.route("/register", methods=["GET", "POST"])
def register():

    #if comers directly GET render the Registration page
    if request.method == 'GET':
        return render_template ("register.html")

    #transfering id's to temp python variable
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    user_fn = request.form.get("user_fn")
    user_ln = request.form.get("user_ln")
    user_city = request.form.get("user_city")
    user_state = request.form.get("user_state")
    user_zip = request.form.get("user_zip")

    #checking if the user already exi or not! if exit return error
    if db.execute("SELECT * FROM register WHERE user_id = :user_id", {"user_id": user_id}).rowcount !=0:
        return render_template("error.html", message="User Already Exited!")

    #inserting into the database user_id, password
    db.execute("INSERT INTO register (user_id, password, user_fn, user_ln, user_city, user_state, user_zip) VALUES (:user_id, :password, :user_fn, :user_ln, :user_city, :user_state, :user_zip)",
            {"user_id": user_id, "password": password, "user_fn" :user_fn, "user_ln" :user_ln, "user_city" :user_city, "user_state" :user_state, "user_zip" :user_zip})

    #finally committing the session (closing the session)
    db.commit()
    return render_template("success.html", message = user_id)

#-------------------------------- END OF Register (Registeration PAGE) --------------------------------------


#-------------------------------- START OF Logout Route (LOGOUT PAGE) --------------------------------------

# Logout Route Basic
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    session.pop('admin_id', None)
    return redirect(url_for('login'))

#-------------------------------- END OF Logout (LOGOUT PAGE) --------------------------------------
