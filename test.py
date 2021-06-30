import csv, os

from sqlalchemy import create_engine
from sqlalchemy import func, extract
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine("postgresql://hqarjmdepnhngt:878b24ec455373807866474ef4b0bcac6f9dd1248e163a61f8ac77bd14c8d556@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d2mjumqpqcetd3")
db = scoped_session(sessionmaker(bind=engine))

def main():
    ctr = 1

    price = db.execute("SELECT * FROM topping").fetchall()
    print(price)
    top_name = db.execute("SELECT top_name FROM topping").fetchall()
    top_name = [name for tup in top_name for name in tup]

    # Working:
    value_customer = db.execute("SELECT cus_id, count(order_id) FROM Orders Group by cus_id").fetchall()
    print("===========================------------------")
    print(value_customer)
    print("===========================------------------\n\n")

    # Working:
    #value_customer = db.execute("SELECT cus_id, ord_dlt.price FROM Orders as ord JOIN Order_details as ord_dlt " +
    #                                "on ord.order_id = ord_dlt.order_id Order by ord_dlt.price DESC LIMIT 5").fetchall()

    value_customer = db.execute("SELECT ord_details.menu_code, ord_details.top_id, sum(ord_details.price) as high_value_order FROM Orders as ord "
    	"INNER JOIN Order_details as ord_details " +
    	"on ord.order_id = ord_details.order_id " +
        "group by ord_details.menu_code, ord_details.top_id " +
    	"Order by sum(ord_details.price) DESC LIMIT 5").fetchall()

    print("===========================------------------")
    print(value_customer)
    v_name = [name for tup in value_customer for name in tup]
    print(v_name)
    print("===========================------------------\n\n")


    # Working:
    # -- Highest Order Range --
    highest_order_range = db.execute("SELECT ord_details.menu_code, ord_details.top_id, sum(ord_details.price) FROM Orders as ord " +
                                    "INNER JOIN Order_details as ord_details " +
                                    "on ord.order_id = ord_details.order_id " +
                                    "group by ord_details.menu_code, ord_details.top_id " +
                                    "Order by sum(ord_details.price) DESC LIMIT 5").fetchall()
    print("===========================------------------")
    print(highest_order_range)
    v_name = [name for tup in highest_order_range for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # ----------------------------------------- SQL 3 ----------------------------------------- #

    # -- Monthly Sales --
    monthly_sales = db.execute("SELECT TO_CHAR(ord.ord_time, 'Month'), sum(ord_details.price) FROM Order_details as ord_details " +
    	                         "INNER JOIN Orders as ord " +
                                 "on ord_details.order_id = ord.order_id "+
                                 "group by TO_CHAR(ord.ord_time, 'Month')").fetchall()
    print("===========================------------------")
    print(monthly_sales)
    v_name = [name for tup in monthly_sales for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # ----------------------------------------- SQL 4 ----------------------------------------- #
    # -- Net Profit --
    net_profit = db.execute("SELECT sup.menu_code, sup.top_id, (pt.p_small - sup.p_small), (pt.p_large - sup.p_large)"
                            "FROM Supplier as sup INNER JOIN Price as pt "
                            "ON (sup.menu_code = pt.menu_code) and (sup.top_id = pt.top_id)").fetchall()
    print("===========================------------------")
    print(net_profit)
    v_name = [name for tup in net_profit for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # ---------------------------------------- SQL 05 -------------------------------------- #
    # -- Most Sold Pizza --
    most_sold_pizza = db.execute("SELECT mn.menu_name, count(ord_details.menu_code) FROM Menu as mn "
                            	"INNER JOIN Order_details as ord_details "
                                "on mn.menu_code = ord_details.menu_code "
                                "group by mn.menu_code").fetchall()
    print("===========================------------------")
    print(most_sold_pizza)
    v_name = [name for tup in most_sold_pizza for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # --------------------

    # ---------------------------------------- SQL 05 -------------------------------------- #
    # -- Most Sold Pizza --
    most_sold_pizza = db.execute("SELECT mn.menu_name, count(ord_details.menu_code) FROM Menu as mn "
                            	"INNER JOIN Order_details as ord_details "
                                "on mn.menu_code = ord_details.menu_code "
                                "group by mn.menu_code").fetchall()

    print("===========================------------------")
    print(most_sold_pizza)
    v_name = [name for tup in most_sold_pizza for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # ---------------------------------------- SQL 05 -------------------------------------- #

    # -- Most Use Topping --
    most_use_topping = db.execute("SELECT tp.top_name, count(ord_details.top_id) FROM Topping as tp "
    	                           "INNER JOIN Order_details as ord_details "
                                   "on tp.top_id = ord_details.top_id "
                                   "group by tp.top_name").fetchall()
    print("===========================------------------")
    print(most_use_topping)
    v_name = [name for tup in most_use_topping for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # --------------------

    # ---------------------------------------- SQL 05 -------------------------------------- #

    # -- Count Valuable Supplier --
    cout_value_supplier = db.execute("SELECT sup_name, count(sup.menu_code) FROM Supplier as sup "
                                	"INNER JOIN order_details as ord_details "
                                	"on (sup.menu_code = ord_details.menu_code) and (sup.top_id = ord_details.top_id) "
                                	"group by sup.sup_name").fetchall()
    print("===========================------------------")
    print(cout_value_supplier)
    v_name = [name for tup in cout_value_supplier for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # ---------------------------------------- SQL 05 -------------------------------------- #

    # -- Lifetime Order --
    lifetime_order = db.execute("SELECT count(order_id) FROM Orders").fetchall()

    print("===========================------------------")
    print(lifetime_order)
    v_name = [name for tup in lifetime_order for name in tup]
    print(v_name)
    print("===========================------------------\n\n")

    # --------------------
    print(top_name)

if __name__ == "__main__":
    main()
